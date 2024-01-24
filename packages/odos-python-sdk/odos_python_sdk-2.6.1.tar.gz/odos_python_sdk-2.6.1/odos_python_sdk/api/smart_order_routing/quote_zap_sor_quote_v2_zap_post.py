from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.path_request_v2 import PathRequestV2
from ...models.quote_response import QuoteResponse
from ...types import Response


def _get_kwargs(
    *,
    body: PathRequestV2,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/sor/quote/v2/zap",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, QuoteResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QuoteResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.BAD_GATEWAY:
        response_502 = cast(Any, None)
        return response_502
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, QuoteResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PathRequestV2,
) -> Response[Union[Any, HTTPValidationError, QuoteResponse]]:
    r"""Generate Odos Zap Quote

     Quote a path for zapping into or out of liquidity positions atomically. Input tokens can be both
    regular ERC-20 tokens and liquidity pool tokens. Outputs can be regular ERC-20 tokens or liquidity
    pool tokens.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `chainId` | Chain ID to use for quote generation. A list of valid chains can be retrieved from
    [`info/chains`](#/Info/get_chain_ids_info_chains_get). | Yes |
    | `inputTokens` | Input tokens and amounts for quote | Yes |
    | `outputTokens`| Output tokens and proportions for quote | Yes |
    | `gasPrice` | Gas price to use for path generation. This price directly affects the path
    computation. If no gas price is provided, our default price from our frontend will be used. | No |
    | `userAddr` | Address of the wallet executing the swap. If no wallet is provided, the quote cannot
    be turned into a path. This can be viewed as informational only. | No |
    | `slippageLimitPercent` | Slippage percent to use for checking if the path is valid. Float.
    Example: to set slippage to 0.5% send `0.5`. If 1% is desired, send `1`. If not provided, slippage
    will be set `0.3`.  | No |
    | `sourceBlacklist` | List of liquidity providers that are not to be used for the swap path. A list
    of all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `sourceWhitelist` | List of liquidity providers to exclusively use for the swap path. A list of
    all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `pathVizImage` | Return a Base64 encoded SVG of path visualization image for display on web
    frontends | No |
    | `pathVizImageConfig` | Optional customization parameters for generated path viz image | No |
    | `disableRFQs` | Disable all exchanges that qualify as RFQs with centralized API dependencies and
    time-sensitive quotes or potential user address restrictions. Default is true. | No |
    | `referralCode` | Code for registering your usage with Odos and receiving partner specific
    benefits. [Referral Code Documentation](https://docs.odos.xyz/product/sor/v2/referral-code) | No |
    | `compact` | Use Odos V2 compact call data for transaction, defaults to `true` | No |
    | `likeAsset` | If input and output tokens are all the same asset type (ex: USD stable coins), only
    route through like assets for decreased slippage. Defaults to `false` | No |
    | `simple` | If a less complicated quote and/or a quicker response time is desired, this flag can be
    set. Defaults to `false` | No |

    ### inputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap from. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `amount` | Amount of the token in fixed precision. String | Yes |


    ### outputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap to. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `proportion` | Percent of token to output. For a single swap, this is set to 1. Float. | Yes |

    ### pathVizImageConfig

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `linkColors` | List of hex codes to generate color spectrum for liquidity sources in path
    visualization | No |
    | `nodeColor` | Hex code for setting the color of token nodes in path visualization | No |
    | `nodeTextColor` | Hex code to set the color of token symbol text on token nodes | No |
    | `legendTextColor` | Hex code to set the color of the visualization legend text | No |
    | `width` | Set a custom width proportion for the visualization | No |
    | `height` | Set a custom height proportion for the visualization | No |

    #### Example Full Config Response:

    ```json
    {
      \"linkColors\": [\"#123456\"],
      \"nodeColor\": \"#1BEEF1\",
      \"nodeTextColor\": \"#FFFFFF\",
      \"legendTextColor\": \"#000000\",
      \"width\": 1200,
      \"height\": 800
    }
    ```

    #### Basic integration:

    Set the `src` attribute of an `<img />` HTML tag to the `pathVizImage` text field of the quote
    response


    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `pathId` | ID of the path used for asking for an assembled quote |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `dataGasEstimate` | Used for Layer 2 chains |
    | `gweiPerGas` | Amount of gWei per gas unit |
    | `inTokens` | A list of token addresses and amounts |
    | `inAmounts` | A list of input token amounts |
    | `outTokens` | A list of token addresses and amounts |
    | `outAmounts` | A list of output token amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `priceImpact` | Percent decrease in the realized price of the path from the initial price of the
    path before the swap is executed. |
    | `percentDiff` | Percent difference between the value of all input tokens and the value of all
    output tokens (as determined by the Odos pricing service) |
    | `partnerFeePercent` | Percent fee taken by partner referral code given. Fee is already deducted
    from quote |
    | `pathVizImage` | Base64 encoded image ready to be used within a UI |

    Args:
        body (PathRequestV2): Public facing path request v2 schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, QuoteResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PathRequestV2,
) -> Optional[Union[Any, HTTPValidationError, QuoteResponse]]:
    r"""Generate Odos Zap Quote

     Quote a path for zapping into or out of liquidity positions atomically. Input tokens can be both
    regular ERC-20 tokens and liquidity pool tokens. Outputs can be regular ERC-20 tokens or liquidity
    pool tokens.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `chainId` | Chain ID to use for quote generation. A list of valid chains can be retrieved from
    [`info/chains`](#/Info/get_chain_ids_info_chains_get). | Yes |
    | `inputTokens` | Input tokens and amounts for quote | Yes |
    | `outputTokens`| Output tokens and proportions for quote | Yes |
    | `gasPrice` | Gas price to use for path generation. This price directly affects the path
    computation. If no gas price is provided, our default price from our frontend will be used. | No |
    | `userAddr` | Address of the wallet executing the swap. If no wallet is provided, the quote cannot
    be turned into a path. This can be viewed as informational only. | No |
    | `slippageLimitPercent` | Slippage percent to use for checking if the path is valid. Float.
    Example: to set slippage to 0.5% send `0.5`. If 1% is desired, send `1`. If not provided, slippage
    will be set `0.3`.  | No |
    | `sourceBlacklist` | List of liquidity providers that are not to be used for the swap path. A list
    of all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `sourceWhitelist` | List of liquidity providers to exclusively use for the swap path. A list of
    all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `pathVizImage` | Return a Base64 encoded SVG of path visualization image for display on web
    frontends | No |
    | `pathVizImageConfig` | Optional customization parameters for generated path viz image | No |
    | `disableRFQs` | Disable all exchanges that qualify as RFQs with centralized API dependencies and
    time-sensitive quotes or potential user address restrictions. Default is true. | No |
    | `referralCode` | Code for registering your usage with Odos and receiving partner specific
    benefits. [Referral Code Documentation](https://docs.odos.xyz/product/sor/v2/referral-code) | No |
    | `compact` | Use Odos V2 compact call data for transaction, defaults to `true` | No |
    | `likeAsset` | If input and output tokens are all the same asset type (ex: USD stable coins), only
    route through like assets for decreased slippage. Defaults to `false` | No |
    | `simple` | If a less complicated quote and/or a quicker response time is desired, this flag can be
    set. Defaults to `false` | No |

    ### inputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap from. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `amount` | Amount of the token in fixed precision. String | Yes |


    ### outputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap to. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `proportion` | Percent of token to output. For a single swap, this is set to 1. Float. | Yes |

    ### pathVizImageConfig

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `linkColors` | List of hex codes to generate color spectrum for liquidity sources in path
    visualization | No |
    | `nodeColor` | Hex code for setting the color of token nodes in path visualization | No |
    | `nodeTextColor` | Hex code to set the color of token symbol text on token nodes | No |
    | `legendTextColor` | Hex code to set the color of the visualization legend text | No |
    | `width` | Set a custom width proportion for the visualization | No |
    | `height` | Set a custom height proportion for the visualization | No |

    #### Example Full Config Response:

    ```json
    {
      \"linkColors\": [\"#123456\"],
      \"nodeColor\": \"#1BEEF1\",
      \"nodeTextColor\": \"#FFFFFF\",
      \"legendTextColor\": \"#000000\",
      \"width\": 1200,
      \"height\": 800
    }
    ```

    #### Basic integration:

    Set the `src` attribute of an `<img />` HTML tag to the `pathVizImage` text field of the quote
    response


    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `pathId` | ID of the path used for asking for an assembled quote |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `dataGasEstimate` | Used for Layer 2 chains |
    | `gweiPerGas` | Amount of gWei per gas unit |
    | `inTokens` | A list of token addresses and amounts |
    | `inAmounts` | A list of input token amounts |
    | `outTokens` | A list of token addresses and amounts |
    | `outAmounts` | A list of output token amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `priceImpact` | Percent decrease in the realized price of the path from the initial price of the
    path before the swap is executed. |
    | `percentDiff` | Percent difference between the value of all input tokens and the value of all
    output tokens (as determined by the Odos pricing service) |
    | `partnerFeePercent` | Percent fee taken by partner referral code given. Fee is already deducted
    from quote |
    | `pathVizImage` | Base64 encoded image ready to be used within a UI |

    Args:
        body (PathRequestV2): Public facing path request v2 schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, QuoteResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PathRequestV2,
) -> Response[Union[Any, HTTPValidationError, QuoteResponse]]:
    r"""Generate Odos Zap Quote

     Quote a path for zapping into or out of liquidity positions atomically. Input tokens can be both
    regular ERC-20 tokens and liquidity pool tokens. Outputs can be regular ERC-20 tokens or liquidity
    pool tokens.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `chainId` | Chain ID to use for quote generation. A list of valid chains can be retrieved from
    [`info/chains`](#/Info/get_chain_ids_info_chains_get). | Yes |
    | `inputTokens` | Input tokens and amounts for quote | Yes |
    | `outputTokens`| Output tokens and proportions for quote | Yes |
    | `gasPrice` | Gas price to use for path generation. This price directly affects the path
    computation. If no gas price is provided, our default price from our frontend will be used. | No |
    | `userAddr` | Address of the wallet executing the swap. If no wallet is provided, the quote cannot
    be turned into a path. This can be viewed as informational only. | No |
    | `slippageLimitPercent` | Slippage percent to use for checking if the path is valid. Float.
    Example: to set slippage to 0.5% send `0.5`. If 1% is desired, send `1`. If not provided, slippage
    will be set `0.3`.  | No |
    | `sourceBlacklist` | List of liquidity providers that are not to be used for the swap path. A list
    of all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `sourceWhitelist` | List of liquidity providers to exclusively use for the swap path. A list of
    all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `pathVizImage` | Return a Base64 encoded SVG of path visualization image for display on web
    frontends | No |
    | `pathVizImageConfig` | Optional customization parameters for generated path viz image | No |
    | `disableRFQs` | Disable all exchanges that qualify as RFQs with centralized API dependencies and
    time-sensitive quotes or potential user address restrictions. Default is true. | No |
    | `referralCode` | Code for registering your usage with Odos and receiving partner specific
    benefits. [Referral Code Documentation](https://docs.odos.xyz/product/sor/v2/referral-code) | No |
    | `compact` | Use Odos V2 compact call data for transaction, defaults to `true` | No |
    | `likeAsset` | If input and output tokens are all the same asset type (ex: USD stable coins), only
    route through like assets for decreased slippage. Defaults to `false` | No |
    | `simple` | If a less complicated quote and/or a quicker response time is desired, this flag can be
    set. Defaults to `false` | No |

    ### inputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap from. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `amount` | Amount of the token in fixed precision. String | Yes |


    ### outputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap to. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `proportion` | Percent of token to output. For a single swap, this is set to 1. Float. | Yes |

    ### pathVizImageConfig

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `linkColors` | List of hex codes to generate color spectrum for liquidity sources in path
    visualization | No |
    | `nodeColor` | Hex code for setting the color of token nodes in path visualization | No |
    | `nodeTextColor` | Hex code to set the color of token symbol text on token nodes | No |
    | `legendTextColor` | Hex code to set the color of the visualization legend text | No |
    | `width` | Set a custom width proportion for the visualization | No |
    | `height` | Set a custom height proportion for the visualization | No |

    #### Example Full Config Response:

    ```json
    {
      \"linkColors\": [\"#123456\"],
      \"nodeColor\": \"#1BEEF1\",
      \"nodeTextColor\": \"#FFFFFF\",
      \"legendTextColor\": \"#000000\",
      \"width\": 1200,
      \"height\": 800
    }
    ```

    #### Basic integration:

    Set the `src` attribute of an `<img />` HTML tag to the `pathVizImage` text field of the quote
    response


    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `pathId` | ID of the path used for asking for an assembled quote |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `dataGasEstimate` | Used for Layer 2 chains |
    | `gweiPerGas` | Amount of gWei per gas unit |
    | `inTokens` | A list of token addresses and amounts |
    | `inAmounts` | A list of input token amounts |
    | `outTokens` | A list of token addresses and amounts |
    | `outAmounts` | A list of output token amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `priceImpact` | Percent decrease in the realized price of the path from the initial price of the
    path before the swap is executed. |
    | `percentDiff` | Percent difference between the value of all input tokens and the value of all
    output tokens (as determined by the Odos pricing service) |
    | `partnerFeePercent` | Percent fee taken by partner referral code given. Fee is already deducted
    from quote |
    | `pathVizImage` | Base64 encoded image ready to be used within a UI |

    Args:
        body (PathRequestV2): Public facing path request v2 schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, QuoteResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PathRequestV2,
) -> Optional[Union[Any, HTTPValidationError, QuoteResponse]]:
    r"""Generate Odos Zap Quote

     Quote a path for zapping into or out of liquidity positions atomically. Input tokens can be both
    regular ERC-20 tokens and liquidity pool tokens. Outputs can be regular ERC-20 tokens or liquidity
    pool tokens.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `chainId` | Chain ID to use for quote generation. A list of valid chains can be retrieved from
    [`info/chains`](#/Info/get_chain_ids_info_chains_get). | Yes |
    | `inputTokens` | Input tokens and amounts for quote | Yes |
    | `outputTokens`| Output tokens and proportions for quote | Yes |
    | `gasPrice` | Gas price to use for path generation. This price directly affects the path
    computation. If no gas price is provided, our default price from our frontend will be used. | No |
    | `userAddr` | Address of the wallet executing the swap. If no wallet is provided, the quote cannot
    be turned into a path. This can be viewed as informational only. | No |
    | `slippageLimitPercent` | Slippage percent to use for checking if the path is valid. Float.
    Example: to set slippage to 0.5% send `0.5`. If 1% is desired, send `1`. If not provided, slippage
    will be set `0.3`.  | No |
    | `sourceBlacklist` | List of liquidity providers that are not to be used for the swap path. A list
    of all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `sourceWhitelist` | List of liquidity providers to exclusively use for the swap path. A list of
    all liquidity providers for a given chain can be retrieved from [`info/liquidity-
    sources/{chain_id}`](#/Info/liquidity_sources_info_liquidity_sources__chain_id__get) | No |
    | `pathVizImage` | Return a Base64 encoded SVG of path visualization image for display on web
    frontends | No |
    | `pathVizImageConfig` | Optional customization parameters for generated path viz image | No |
    | `disableRFQs` | Disable all exchanges that qualify as RFQs with centralized API dependencies and
    time-sensitive quotes or potential user address restrictions. Default is true. | No |
    | `referralCode` | Code for registering your usage with Odos and receiving partner specific
    benefits. [Referral Code Documentation](https://docs.odos.xyz/product/sor/v2/referral-code) | No |
    | `compact` | Use Odos V2 compact call data for transaction, defaults to `true` | No |
    | `likeAsset` | If input and output tokens are all the same asset type (ex: USD stable coins), only
    route through like assets for decreased slippage. Defaults to `false` | No |
    | `simple` | If a less complicated quote and/or a quicker response time is desired, this flag can be
    set. Defaults to `false` | No |

    ### inputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap from. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `amount` | Amount of the token in fixed precision. String | Yes |


    ### outputTokens

    | Parameter | Description | Required |
    | --- | --- | --- |
    | `tokenAddress` | Address of the token to swap to. This should be a [checksummed
    address](https://eips.ethereum.org/EIPS/eip-55). | Yes |
    | `proportion` | Percent of token to output. For a single swap, this is set to 1. Float. | Yes |

    ### pathVizImageConfig

    | Parameter | Description | Required |
    | --- | ------------- | --- |
    | `linkColors` | List of hex codes to generate color spectrum for liquidity sources in path
    visualization | No |
    | `nodeColor` | Hex code for setting the color of token nodes in path visualization | No |
    | `nodeTextColor` | Hex code to set the color of token symbol text on token nodes | No |
    | `legendTextColor` | Hex code to set the color of the visualization legend text | No |
    | `width` | Set a custom width proportion for the visualization | No |
    | `height` | Set a custom height proportion for the visualization | No |

    #### Example Full Config Response:

    ```json
    {
      \"linkColors\": [\"#123456\"],
      \"nodeColor\": \"#1BEEF1\",
      \"nodeTextColor\": \"#FFFFFF\",
      \"legendTextColor\": \"#000000\",
      \"width\": 1200,
      \"height\": 800
    }
    ```

    #### Basic integration:

    Set the `src` attribute of an `<img />` HTML tag to the `pathVizImage` text field of the quote
    response


    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `pathId` | ID of the path used for asking for an assembled quote |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `dataGasEstimate` | Used for Layer 2 chains |
    | `gweiPerGas` | Amount of gWei per gas unit |
    | `inTokens` | A list of token addresses and amounts |
    | `inAmounts` | A list of input token amounts |
    | `outTokens` | A list of token addresses and amounts |
    | `outAmounts` | A list of output token amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `priceImpact` | Percent decrease in the realized price of the path from the initial price of the
    path before the swap is executed. |
    | `percentDiff` | Percent difference between the value of all input tokens and the value of all
    output tokens (as determined by the Odos pricing service) |
    | `partnerFeePercent` | Percent fee taken by partner referral code given. Fee is already deducted
    from quote |
    | `pathVizImage` | Base64 encoded image ready to be used within a UI |

    Args:
        body (PathRequestV2): Public facing path request v2 schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, QuoteResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
