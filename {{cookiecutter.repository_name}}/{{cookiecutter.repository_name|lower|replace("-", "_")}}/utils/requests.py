from enum import StrEnum
from typing import Optional

import httpx
from httpx import AsyncClient, Response
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger import Logger, LoggerFactory
from {{cookiecutter.repository_name|lower|replace("-", "_")}}.settings import RETRY_AFTER_SECONDS, RETRY_ATTEMPTS

_logger: Logger = LoggerFactory.new()


class MethodRequestEnum(StrEnum):
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'
    PUT = 'put'
    DELETE = 'delete'


@retry(
    reraise=True,
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_fixed(RETRY_AFTER_SECONDS),
    retry=retry_if_exception_type(ConnectionError),
)
async def make_async_request(
    method: MethodRequestEnum,
    url: str,
    *,
    data: dict | None = None,
    json: dict | None = None,
    params: dict | None = None,
    headers: dict | None = None,
    authorization: str | None = None,
    files: list[tuple[str, tuple[str, bytes]]] = None,
    timeout: int = 120,
    auth: tuple[str, str] | None = None,
    follow_redirects: bool = True,
    raise_for_status: bool = True,
) -> Response:
    _logger.debug(
        'Making async request...',
        data=dict(
            method=method,
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            authorization=authorization,
            files=files,
            timeout=timeout,
            auth=auth,
            follow_redirects=follow_redirects,
        ),
    )

    if authorization and isinstance(headers, dict):
        headers['Authorization'] = authorization

    async with AsyncClient() as client:
        response = await client.request(
            method,
            url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            timeout=timeout,
            auth=auth,
            files=files,
            follow_redirects=follow_redirects,
        )
    if raise_for_status:
        response.raise_for_status()
    return response


@retry(
    reraise=True,
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_fixed(RETRY_AFTER_SECONDS),
    retry=retry_if_exception_type(ConnectionError),
)
def make_request(
    method: MethodRequestEnum,
    url: str,
    *,
    data: dict | None = None,
    json: dict | None = None,
    params: dict | None = None,
    headers: dict | None = None,
    authorization: str | None = None,
    files: list[tuple[str, tuple[str, bytes]]] = None,
    timeout: int = 120,
    auth: Optional[tuple[str, str]] = None,
    follow_redirects: bool = True,
    raise_for_status: bool = True,
) -> Response:
    _logger.debug(
        'Making request...',
        data=dict(
            method=method,
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            authorization=authorization,
            files=files,
            timeout=timeout,
            auth=auth,
            follow_redirects=follow_redirects,
        ),
    )

    if authorization and isinstance(headers, dict):
        headers['Authorization'] = authorization

    response = httpx.request(
        method,
        url,
        data=data,
        json=data,
        params=params,
        headers=headers,
        timeout=timeout,
        auth=auth,
        files=files,
        follow_redirects=follow_redirects,
    )
    if raise_for_status:
        response.raise_for_status()

    return response
