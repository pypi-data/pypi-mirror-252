from __future__ import annotations

import asyncio
import os
import random
import weakref
from collections.abc import AsyncGenerator, Coroutine, Generator, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from functools import partial, wraps
from http import HTTPStatus
from typing import Any, Callable, Optional, Union

import httpx
from dateutil.parser import isoparse

import arraylake
from arraylake import config as config_obj
from arraylake.asyn import close_async_context, get_loop, sync
from arraylake.diagnostics import get_diagnostics
from arraylake.log_util import get_logger
from arraylake.token import AuthException, TokenHandler
from arraylake.types import ApiTokenInfo, OauthTokensResponse, UserInfo

HTTP_TIMEOUT = int(os.environ.get("ARRAYLAKE_HTTP_TIMEOUT", 300))


logger = get_logger(__name__)


# this is a hashable key to use for the global client cache
# we only need one client for each key
@dataclass(eq=True, frozen=True)
class ClientKey:
    loop: asyncio.AbstractEventLoop
    api_url: str
    auth_key: int  # hash(token)
    hint: Optional[str]
    headers: tuple[tuple[str, str], ...]
    timeout: int


# the global cache of httpx clients
_GLOBAL_CLIENTS: dict[ClientKey, httpx.AsyncClient] = {}

# this is a cache to use hold asyncio tasks so they are not garbage collected before finishing
background_tasks: set[asyncio.Task] = set()


async def get_client(
    loop: asyncio.AbstractEventLoop, api_url: str, token: Optional[str], hint: Optional[str], headers: Mapping[str, str], timeout: int
) -> httpx.AsyncClient:
    """
    Attempt to get an httpx client for a specific event loop and set of parameters.
    If the client already exists, the global cache will be used.
    If not, a new client will be created.
    """
    auth: httpx.Auth

    # we need to set up auth every time this function is called in case the user has logged out
    if token is None:
        # if a token is presented, just use that token for all all Authentication headers
        auth = UserAuth(api_url, hint)
        auth_key = hash(auth._token_handler.tokens)
    else:
        # otherwise, assume we are using OAuth tokens stored on disk
        auth = TokenAuth(token)
        auth_key = hash(token)

    key = ClientKey(loop, api_url, auth_key, hint, tuple(sorted(headers.items())), timeout)
    logger.debug("%i httpx clients present in cache.", len(_GLOBAL_CLIENTS))
    if key not in _GLOBAL_CLIENTS:
        logger.debug("Creating new httpx client %s. Loop id %s.", key, id(loop))
        transport = AsyncRetryTransport()
        client = await httpx.AsyncClient(base_url=api_url, transport=transport, headers=headers, auth=auth, timeout=timeout).__aenter__()
        weakref.finalize(client, close_client, key)
        _GLOBAL_CLIENTS[key] = client
    else:
        logger.debug("Client %s already present. Loop id %s.", key, id(loop))
    return _GLOBAL_CLIENTS[key]


def close_client(key: ClientKey):
    """
    This is a finalizer function that is called when a global client is
    garbage collected. It cleanly closes the client for the specified key.

    If the event loop associated with this client is determined to be the
    dedicated io loop, we call `sync` to on __aexit__.

    If the event loop associated with this client is determined to be the currently
    running event loop, we schedule the __aexit__ coroutine for execution.

    If the event loop doesn't match any of these scenarios, we have no way to call
    the closer function and issue a RuntimeWarning

    Note: logging in this function runs the risk of conflicting with pytest#5502. For
    this reason, we have removed debug log statements.
    """
    client = _GLOBAL_CLIENTS.pop(key)

    if client.is_closed:
        return

    client_loop = key.loop  # the loop this client was created from

    sync_loop = get_loop()  # the loop associated with the synchronizer thread

    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if client_loop.is_closed():
        # This is the most common path followed in our test suite.
        # We are never able to explicitly close the httpx client and associated connection pool.
        # But we don't see any errors or warnings, so I guess it's fine?
        pass
    else:
        # client loop is still open -- how can we talk to it?
        if client_loop is sync_loop:
            sync(close_async_context, client, "calling from sync", timeout=1)
        elif client_loop is running_loop:
            coro = close_async_context(client, f"closing from loop {id(client_loop)}")
            if client_loop.is_running():
                task = client_loop.create_task(coro)
                # try to prevent this task from being garbage collected before it finishes
                background_tasks.add(task)
            else:
                client_loop.run_until_complete(coro)


def calc_backoff(attempt: int, *, backoff_factor: float, jitter_ratio: float, max_backoff_wait: float) -> float:
    """Calculate a backoff time in seconds based on the attempt number"""
    if attempt < 1:
        return 0.0

    assert backoff_factor >= 0
    assert jitter_ratio >= 0
    assert max_backoff_wait >= 0

    backoff = backoff_factor * (2 ** (attempt - 1))
    jitter = (backoff * jitter_ratio) * random.choice([1.0, -1.0])
    total_backoff = backoff + jitter
    return min(total_backoff, max_backoff_wait)


def retry_on_exception(exceptions: type[Exception] | tuple[type[Exception], ...], n: int) -> Callable:
    """Retry a function when a specific exception is raised

    Intended to be used as a decorator. For example:

    @retry_on_exception((ValueError, ), n=3)
    async def raise_value_error():
        raise ValueError

    If the exception is re-raised `n` times, the final exception is returned.

    A exponentially increasing backoff (with jitter) is used between retries.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if i == n - 1:
                        logger.debug(f"{type(e)} encountered with all retries. failing.")
                        raise e
                    backoff = calc_backoff(i + 1, backoff_factor=0.5, jitter_ratio=0.1, max_backoff_wait=10)
                    logger.debug(f"{type(e)} encountered, retrying time #{i} after {backoff} seconds")
                    await asyncio.sleep(backoff)  # try again after a pause

        return wrapper

    return decorator


async def gather_and_check_for_exceptions(*aws):
    """helper function to call asyncio.gather on a list of awaitables and check if any returned an exception"""
    results = await asyncio.gather(*aws, return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            raise r  # is only raising on the first error ok?
    return results


class ArraylakeHttpClient:
    """Base class to centralize interacting with Arraylake REST API"""

    api_url: str
    hint: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)  # machine token. id/access/refresh tokens are managed by CustomOauth
    timeout: int = HTTP_TIMEOUT

    _client: Optional[httpx.AsyncClient]
    _OPEN: bool

    def __init__(self, api_url: str, hint: Optional[str] = None, token: Optional[str] = None, managed_sessions: bool = False):
        self.api_url = api_url
        self.hint = hint
        self.token = token

        self.managed_sessions = managed_sessions or config_obj.config.get("server_managed_sessions", False)

        self._default_headers = {
            "accept": "application/vnd.earthmover+json",
            # technically we don't enforce this, for now it's for debugging purposes
            "client-name": "arraylake-python-client",
            "client-version": arraylake.__version__,
            # TODO: Remove this once managed sessions are mandatory for all users.
            "arraylake-feature-managed-sessions": str(self.managed_sessions),
        }

        self._client = None

    def __getstate__(self):
        return self.api_url, self.hint, self.token, self._default_headers

    def __setstate__(self, state):
        self.api_url, self.hint, self.token, self._default_headers = state
        self._client = None

    @retry_on_exception((httpx.RemoteProtocolError, httpx.ConnectError), 3)
    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Convenience method to make a standard request with retry on RemoteProtocolError"""
        if self._client is None:
            loop = asyncio.get_running_loop()
            self._client = await get_client(loop, self.api_url, self.token, self.hint, self._default_headers, self.timeout)
        return await self._client.request(method, path, **kwargs)

    async def get_user(self) -> Union[ApiTokenInfo, UserInfo]:
        """Make an API request to the /user route to get the current authenticated user

        This is used in various places through the Arraylake client. For example, we use this method to:
        - determine the committer/author when creating a repo instance
        - check if a user is logged in with valid credentials

        This method also sends a package of run-time diagnostics to the server.

        TODO: consider moving this to the Client API.
        """

        response = await self._request("GET", "user")
        handle_response(response)
        data = response.json()

        # get some basic user session diagnostics and pack them as JSON
        if config_obj.config.get("user.diagnostics", True):
            try:
                diagnostics = get_diagnostics()
                response = await self._request("POST", "user/diagnostics", content=diagnostics.model_dump_json())
                handle_response(response)
            except Exception as e:
                await logger.adebug("failed to send diagnostics", exception=str(e))

        # TODO: It would be preferable to have a firmer way to evaluate this
        # perhaps via an explicit type property included with the response
        # object.
        if "first_name" in data:
            return UserInfo(**data)
        else:
            return ApiTokenInfo(**data)


def _exception_log_debug(request: httpx.Request, response: httpx.Response):
    """Utility function to log data pertaining to a failed req/response"""
    secret_headers = {"authorization"}
    clean_request_headers = {n: ("[omitted]" if n.lower() in secret_headers else v) for n, v in request.headers.items()}
    clean_response_headers = {n: ("[omitted]" if n.lower() in secret_headers else v) for n, v in response.headers.items()}
    logger.debug(
        "HTTP request failure debug information",
        url=str(request.url),
        request_content=request.content,
        request_headers=clean_request_headers,
        response_headers=clean_response_headers,
        response_status_code=response.status_code,
    )


def handle_response(response: httpx.Response):
    """Convenience function to handle response status codes"""
    try:
        response.raise_for_status()
    except httpx.RequestError as exc:
        _exception_log_debug(exc.request, response)
        raise RuntimeError(f"An error occurred while requesting {exc.request.url!r}. {response}: {response.text}")
    except httpx.HTTPStatusError as exc:
        _exception_log_debug(exc.request, response)
        # we can consider a 422 an explicit message from the serves that something was invalid but handled about
        # the user input, and surface this directly to the caller. for other, less clear cases,
        # return a more complete message including the API url.
        if exc.response.status_code == 422:
            raise ValueError(response.json()["detail"])
        else:
            raise ValueError(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. {response}: {response.text}")


@dataclass(frozen=True)
class TokenAuth(httpx.Auth):
    """
    Simple token-based Auth

    This auth flow will insert a Bearer token into the Authorization header of each request.

    Parameters
    ----------
    token : str
        Token to be inserted into request headers.
    """

    token: str

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        # Send the request, with a bearer token header
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class UserAuth(httpx.Auth):
    """
    User / Oauth token-based Auth

    Parameters
    ----------
    api_endpoint : str
    """

    requires_response_body = True

    def __init__(self, api_endpoint: str, hint: Optional[str] = None):
        self.api_endpoint = api_endpoint
        self.hint = hint
        self._refresh_url = f"{api_endpoint}/refresh_token"

        # self._sync_lock = threading.RLock()  # uncomment when we need sync_auth_flow
        self._async_lock = asyncio.Lock()

        self._token_handler = TokenHandler(api_endpoint=api_endpoint, hint=self.hint, raise_if_not_logged_in=True)

    @property
    def _bearer_token(self):
        if self._token_handler.tokens is None:
            raise AuthException("Not logged in, please log in with `arraylake auth login`")
        token = self._token_handler.tokens.id_token.get_secret_value()
        return f"Bearer {token}"

    def build_refresh_request(self) -> httpx.Request:
        # Return an `httpx.Request` for refreshing tokens.
        if self._token_handler.tokens is None:
            raise AuthException("Must be logged in to refresh tokens")
        params = {"token": self._token_handler.tokens.refresh_token.get_secret_value()}
        if self.hint:
            params["hint"] = self.hint
        request = httpx.Request("GET", self._refresh_url, params=params)
        return request

    async def async_auth_flow(self, request: httpx.Request) -> AsyncGenerator[httpx.Request, httpx.Response]:
        request.headers["Authorization"] = self._bearer_token
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            # If the server issues a 401 response, then issue a request to
            # refresh tokens, and resend the request.
            async with self._async_lock:
                refresh_response = yield self.build_refresh_request()
                await refresh_response.aread()
                handle_response(refresh_response)
                new_tokens = OauthTokensResponse.model_validate_json(refresh_response.content)
                self._token_handler.update(new_tokens)

            request.headers["Authorization"] = self._bearer_token
            yield request

    def sync_auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        # we can implement this method if we end up needing the sync httpx.Client
        raise RuntimeError("Sync auth flow not implemented yet")


# Copied and modified from https://github.com/encode/httpx/issues/108#issuecomment-1434439481
@dataclass
class AsyncRetryTransport(httpx.AsyncBaseTransport):
    max_attempts: int = int(config_obj.config.get("http_max_retries", 15))
    max_backoff_wait: float = 10
    backoff_factor: float = 0.1  # seconds, doubled every retry
    jitter_ratio: float = 0.1
    respect_retry_after_header: bool = True
    retryable_methods: frozenset[str] = field(default=frozenset(["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"]))
    retry_status_codes: frozenset[int] = field(
        default=frozenset(
            [HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.BAD_GATEWAY, HTTPStatus.SERVICE_UNAVAILABLE, HTTPStatus.GATEWAY_TIMEOUT]
        )
    )
    """
    A custom HTTP transport that automatically retries requests using an exponential backoff strategy
    for specific HTTP status codes and request methods.

    Args:
        wrapped_transport (Union[httpx.BaseTransport, httpx.AsyncBaseTransport]): The underlying HTTP transport
            to wrap and use for making requests.
        max_attempts (int, optional): The maximum number of times to retry a request before giving up. Defaults to 10.
        initial_backoff_wait (float, optional): The initial backoff time in seconds. Defaults to 0.1.
        max_backoff_wait (float, optional): The maximum time to wait between retries in seconds. Defaults to 60.
        backoff_factor (float, optional): The factor by which the wait time increases with each retry attempt.
            Defaults to 0.1.
        jitter_ratio (float, optional): The amount of jitter to add to the backoff time. Jitter is a random
            value added to the backoff time to avoid a "thundering herd" effect. The value should be between 0 and 0.5.
            Defaults to 0.1.
        respect_retry_after_header (bool, optional): Whether to respect the Retry-After header in HTTP responses
            when deciding how long to wait before retrying. Defaults to True.
        retryable_methods (Iterable[str], optional): The HTTP methods that can be retried. Defaults to
            ["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"].
        retry_status_codes (Iterable[int], optional): The HTTP status codes that can be retried. Defaults to
            [429, 502, 503, 504].
    """

    def __post_init__(self) -> None:
        if self.jitter_ratio < 0 or self.jitter_ratio > 0.5:
            raise ValueError(f"Jitter ratio should be between 0 and 0.5, actual {self.jitter_ratio}")
        self.wrapped_transport = httpx.AsyncHTTPTransport()

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Sends an HTTP request, possibly with retries.

        Args:
            request: The request to perform.

        Returns:
            The response.

        """
        transport: httpx.AsyncBaseTransport = self.wrapped_transport
        if request.method in self.retryable_methods:
            send_method = partial(transport.handle_async_request)
            response = await self._retry_operation_async(request, send_method)
        else:
            response = await transport.handle_async_request(request)
        return response

    async def aclose(self) -> None:
        """
        Closes the underlying HTTP transport, terminating all outstanding connections and rejecting any further
        requests.

        This should be called before the object is dereferenced, to ensure that connections are properly cleaned up.
        """
        transport: httpx.AsyncBaseTransport = self.wrapped_transport
        await transport.aclose()

    def _calculate_sleep(self, attempts_made: int, headers: Union[httpx.Headers, Mapping[str, str]]) -> float:
        # Retry-After
        # The Retry-After response HTTP header indicates how long the user agent should wait before
        # making a follow-up request. There are three main cases this header is used:
        # - When sent with a 503 (Service Unavailable) response, this indicates how long the service
        #   is expected to be unavailable.
        # - When sent with a 429 (Too Many Requests) response, this indicates how long to wait before
        #   making a new request.
        # - When sent with a redirect response, such as 301 (Moved Permanently), this indicates the
        #   minimum time that the user agent is asked to wait before issuing the redirected request.
        retry_after_header = (headers.get("Retry-After") or "").strip()
        if self.respect_retry_after_header and retry_after_header:
            if retry_after_header.isdigit():
                return float(retry_after_header)

            try:
                parsed_date = isoparse(retry_after_header).astimezone()  # converts to local time
                diff = (parsed_date - datetime.now().astimezone()).total_seconds()
                if diff > 0:
                    return min(diff, self.max_backoff_wait)
            except ValueError:
                pass

        # note, this is never called for attempts_made == 0
        return calc_backoff(
            attempts_made, backoff_factor=self.backoff_factor, jitter_ratio=self.jitter_ratio, max_backoff_wait=self.max_backoff_wait
        )

    async def _retry_operation_async(
        self,
        request: httpx.Request,
        send_method: Callable[..., Coroutine[Any, Any, httpx.Response]],
    ) -> httpx.Response:
        remaining_attempts = self.max_attempts
        attempts_made = 0
        headers = {}  # type: Union[httpx.Headers, Mapping[str, str]]
        while True:
            if attempts_made > 0:
                await asyncio.sleep(self._calculate_sleep(attempts_made, headers))
            response = await send_method(request)
            headers = response.headers
            if remaining_attempts < 1 or response.status_code not in self.retry_status_codes:
                return response
            await response.aclose()
            attempts_made += 1
            remaining_attempts -= 1
