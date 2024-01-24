from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chain_token_price_map import ChainTokenPriceMap
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    *,
    token_addresses: Union[Unset, List[str]] = UNSET,
    currency_id: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_token_addresses: Union[Unset, List[str]] = UNSET
    if not isinstance(token_addresses, Unset):
        json_token_addresses = token_addresses

    params["token_addresses"] = json_token_addresses

    json_currency_id: Union[None, Unset, str]
    if isinstance(currency_id, Unset):
        json_currency_id = UNSET
    else:
        json_currency_id = currency_id
    params["currencyId"] = json_currency_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/pricing/token/{chain_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChainTokenPriceMap, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChainTokenPriceMap.from_dict(response.json())

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
) -> Response[Union[ChainTokenPriceMap, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    token_addresses: Union[Unset, List[str]] = UNSET,
    currency_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[ChainTokenPriceMap, HTTPValidationError]]:
    """Get all chain whitelisted token prices, unless list is specified

     Get all of the whitelisted token prices on an Odos supported chain

    Args:
        chain_id (int):
        token_addresses (Union[Unset, List[str]]):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChainTokenPriceMap, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_addresses=token_addresses,
        currency_id=currency_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    token_addresses: Union[Unset, List[str]] = UNSET,
    currency_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ChainTokenPriceMap, HTTPValidationError]]:
    """Get all chain whitelisted token prices, unless list is specified

     Get all of the whitelisted token prices on an Odos supported chain

    Args:
        chain_id (int):
        token_addresses (Union[Unset, List[str]]):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChainTokenPriceMap, HTTPValidationError]
    """

    return sync_detailed(
        chain_id=chain_id,
        client=client,
        token_addresses=token_addresses,
        currency_id=currency_id,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    token_addresses: Union[Unset, List[str]] = UNSET,
    currency_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[ChainTokenPriceMap, HTTPValidationError]]:
    """Get all chain whitelisted token prices, unless list is specified

     Get all of the whitelisted token prices on an Odos supported chain

    Args:
        chain_id (int):
        token_addresses (Union[Unset, List[str]]):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChainTokenPriceMap, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_addresses=token_addresses,
        currency_id=currency_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    token_addresses: Union[Unset, List[str]] = UNSET,
    currency_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ChainTokenPriceMap, HTTPValidationError]]:
    """Get all chain whitelisted token prices, unless list is specified

     Get all of the whitelisted token prices on an Odos supported chain

    Args:
        chain_id (int):
        token_addresses (Union[Unset, List[str]]):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChainTokenPriceMap, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            client=client,
            token_addresses=token_addresses,
            currency_id=currency_id,
        )
    ).parsed
