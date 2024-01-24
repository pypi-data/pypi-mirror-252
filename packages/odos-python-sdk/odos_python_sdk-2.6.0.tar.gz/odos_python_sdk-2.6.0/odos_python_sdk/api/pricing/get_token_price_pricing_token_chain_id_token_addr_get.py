from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.token_price import TokenPrice
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    token_addr: str,
    *,
    currency_id: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_currency_id: Union[None, Unset, str]
    if isinstance(currency_id, Unset):
        json_currency_id = UNSET
    else:
        json_currency_id = currency_id
    params["currencyId"] = json_currency_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/pricing/token/{chain_id}/{token_addr}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TokenPrice]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenPrice.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TokenPrice]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chain_id: int,
    token_addr: str,
    *,
    client: Union[AuthenticatedClient, Client],
    currency_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TokenPrice]]:
    """Get single token price

     Get the token price info for a given chain and address. Price will be null if asset is valid but
    price is not available

    Args:
        chain_id (int):
        token_addr (str):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenPrice]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_addr=token_addr,
        currency_id=currency_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chain_id: int,
    token_addr: str,
    *,
    client: Union[AuthenticatedClient, Client],
    currency_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TokenPrice]]:
    """Get single token price

     Get the token price info for a given chain and address. Price will be null if asset is valid but
    price is not available

    Args:
        chain_id (int):
        token_addr (str):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenPrice]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_addr=token_addr,
        client=client,
        currency_id=currency_id,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    token_addr: str,
    *,
    client: Union[AuthenticatedClient, Client],
    currency_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TokenPrice]]:
    """Get single token price

     Get the token price info for a given chain and address. Price will be null if asset is valid but
    price is not available

    Args:
        chain_id (int):
        token_addr (str):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenPrice]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_addr=token_addr,
        currency_id=currency_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    token_addr: str,
    *,
    client: Union[AuthenticatedClient, Client],
    currency_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TokenPrice]]:
    """Get single token price

     Get the token price info for a given chain and address. Price will be null if asset is valid but
    price is not available

    Args:
        chain_id (int):
        token_addr (str):
        currency_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenPrice]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_addr=token_addr,
            client=client,
            currency_id=currency_id,
        )
    ).parsed
