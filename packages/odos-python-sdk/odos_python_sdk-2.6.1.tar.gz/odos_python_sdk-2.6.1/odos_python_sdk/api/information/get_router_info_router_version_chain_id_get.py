from http import HTTPStatus
from typing import Any, Dict, Literal, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.router_address import RouterAddress
from ...types import Response


def _get_kwargs(
    version: Literal["v2"],
    chain_id: int,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/info/router/{version}/{chain_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, RouterAddress]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RouterAddress.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, RouterAddress]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    version: Literal["v2"],
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, RouterAddress]]:
    """Address of the Odos router for given chain and version

     Address of Odos router contract that a swap path must be sent to.

    Args:
        version (Literal['v2']): Odos API supported versions
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RouterAddress]]
    """

    kwargs = _get_kwargs(
        version=version,
        chain_id=chain_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    version: Literal["v2"],
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, RouterAddress]]:
    """Address of the Odos router for given chain and version

     Address of Odos router contract that a swap path must be sent to.

    Args:
        version (Literal['v2']): Odos API supported versions
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RouterAddress]
    """

    return sync_detailed(
        version=version,
        chain_id=chain_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    version: Literal["v2"],
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, RouterAddress]]:
    """Address of the Odos router for given chain and version

     Address of Odos router contract that a swap path must be sent to.

    Args:
        version (Literal['v2']): Odos API supported versions
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RouterAddress]]
    """

    kwargs = _get_kwargs(
        version=version,
        chain_id=chain_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    version: Literal["v2"],
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, RouterAddress]]:
    """Address of the Odos router for given chain and version

     Address of Odos router contract that a swap path must be sent to.

    Args:
        version (Literal['v2']): Odos API supported versions
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RouterAddress]
    """

    return (
        await asyncio_detailed(
            version=version,
            chain_id=chain_id,
            client=client,
        )
    ).parsed
