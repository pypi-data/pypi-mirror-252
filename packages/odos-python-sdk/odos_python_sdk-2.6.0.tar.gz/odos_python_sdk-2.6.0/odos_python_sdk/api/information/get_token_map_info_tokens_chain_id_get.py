from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.token_map import TokenMap
from ...types import Response


def _get_kwargs(
    chain_id: int,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/info/tokens/{chain_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TokenMap]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenMap.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TokenMap]]:
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
) -> Response[Union[HTTPValidationError, TokenMap]]:
    """Tokens supported by Odos

     All of the supported ERC-20 tokens that Odos uses for swaps for input, output, and routing tokens.
    These tokens have been manually audited to ensure they will work with Odos. Custom tokens can also
    be used with Odos, but there is no guarantee Odos will find a valid path.

    Please reach out if there is a token that should be added to Odos' natively supported tokens.

    Args:
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenMap]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, TokenMap]]:
    """Tokens supported by Odos

     All of the supported ERC-20 tokens that Odos uses for swaps for input, output, and routing tokens.
    These tokens have been manually audited to ensure they will work with Odos. Custom tokens can also
    be used with Odos, but there is no guarantee Odos will find a valid path.

    Please reach out if there is a token that should be added to Odos' natively supported tokens.

    Args:
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenMap]
    """

    return sync_detailed(
        chain_id=chain_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, TokenMap]]:
    """Tokens supported by Odos

     All of the supported ERC-20 tokens that Odos uses for swaps for input, output, and routing tokens.
    These tokens have been manually audited to ensure they will work with Odos. Custom tokens can also
    be used with Odos, but there is no guarantee Odos will find a valid path.

    Please reach out if there is a token that should be added to Odos' natively supported tokens.

    Args:
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenMap]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, TokenMap]]:
    """Tokens supported by Odos

     All of the supported ERC-20 tokens that Odos uses for swaps for input, output, and routing tokens.
    These tokens have been manually audited to ensure they will work with Odos. Custom tokens can also
    be used with Odos, but there is no guarantee Odos will find a valid path.

    Please reach out if there is a token that should be added to Odos' natively supported tokens.

    Args:
        chain_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenMap]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            client=client,
        )
    ).parsed
