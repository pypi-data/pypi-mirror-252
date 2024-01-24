from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assemble_path_request import AssemblePathRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.path_response import PathResponse
from ...types import Response


def _get_kwargs(
    *,
    body: AssemblePathRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/sor/assemble",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, PathResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PathResponse.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, PathResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AssemblePathRequest,
) -> Response[Union[Any, HTTPValidationError, PathResponse]]:
    """Assemble Odos quote into transaction

     Provide valid call data for a given quoted path. This is called after calling the `sor/quote`
    endpoint and receiving back a quote and `pathID`.

    A quote only lasts for 60 seconds. If it is not assembled in that time, it will not be available to
    assemble, and the path will need to be quoted again.

    Use the information provided by this endpoint directly. Do not try to modify the call data. You will
    make a mistake and you will end up losing money. **We will not provide support for users modifying
    the call data provided by our API.** The data the API provides is directly able to be executed on
    chain.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------- | --- |
    | `userAddr` | Address of the user who requested the quote | Yes |
    | `pathId` | ID of the Path returned from the `sor/quote/{version}` endpoint | Yes |
    | `simulate` | Simulate the transaction to make sure it can actually be executed. This increases the
    response time to receive transaction data. Defaults to False. | No |
    | `receiver` | Optionally, specify a different receiver address for the transaction output, default
    receiver is `userAddr` | No |

    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `inputTokens` | List of input token addresses and amounts |
    | `outputTokens` | List of output token addresses and amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `transaction` | Transaction data needed for execution |
    | `simulation` | Simulation results |

    ### Transaction

    This structure can be signed by a wallet and be executed against the Odos router.

    In the smart contract that makes the swap, the `data` field of the transaction given in the response
    can be used in a low level call from another contract:

    ```solidity
    (bool success, bytes memory result) = router.call{value: $ethInput}(data)
    ```

    Where `$ethInput` is `0` unless the native coin of the network is an input, in which case the value
    should be set to the corresponding path input amount. Approvals for ERC20 inputs should be made to
    the router address prior to the call. The address of the router can be found in the `to` field of
    the response, as well as from the `/info/router/{version}/{chain_id}` endpoint.

    | Parameter | Description |
    | --- | --- |
    | `chainId` | The chain ID for the path to execute one |
    | `gas` | Suggested gas limit. Either 2X the naive gas estimate or 10% more than the simulated gas
    estimate |
    | `gasPrice` | Gas price used to calculate the path |
    | `value` | Input amount of gas token. 0 if the gas token is not one of the inputs |
    | `to` | Odos router address to be used for the transaction |
    | `from` | Source of the executed transaction |
    | `data` | Call data for the Odos router. This is the payload used by our executor contracts to
    execute the necessary DEX swaps. |
    | `nonce` | The standard ETH nonce |


    ### Simulation

    This the result of the simulation

    | Parameter | Description |
    | --- | --- |
    | `isSuccess` | If the transaction reverted or not |
    | `amountsOut` | Amounts out when the path was simulated |
    | `simGasUsed` | Gas used by the simulation |
    | `gasEstimate` | Estimate from a `eth_estimateGas` RPC call for the path |
    | `simulationError` | If a simulation error occurs, it will show up here. |

    Args:
        body (AssemblePathRequest): Assemble Path Request Schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PathResponse]]
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
    body: AssemblePathRequest,
) -> Optional[Union[Any, HTTPValidationError, PathResponse]]:
    """Assemble Odos quote into transaction

     Provide valid call data for a given quoted path. This is called after calling the `sor/quote`
    endpoint and receiving back a quote and `pathID`.

    A quote only lasts for 60 seconds. If it is not assembled in that time, it will not be available to
    assemble, and the path will need to be quoted again.

    Use the information provided by this endpoint directly. Do not try to modify the call data. You will
    make a mistake and you will end up losing money. **We will not provide support for users modifying
    the call data provided by our API.** The data the API provides is directly able to be executed on
    chain.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------- | --- |
    | `userAddr` | Address of the user who requested the quote | Yes |
    | `pathId` | ID of the Path returned from the `sor/quote/{version}` endpoint | Yes |
    | `simulate` | Simulate the transaction to make sure it can actually be executed. This increases the
    response time to receive transaction data. Defaults to False. | No |
    | `receiver` | Optionally, specify a different receiver address for the transaction output, default
    receiver is `userAddr` | No |

    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `inputTokens` | List of input token addresses and amounts |
    | `outputTokens` | List of output token addresses and amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `transaction` | Transaction data needed for execution |
    | `simulation` | Simulation results |

    ### Transaction

    This structure can be signed by a wallet and be executed against the Odos router.

    In the smart contract that makes the swap, the `data` field of the transaction given in the response
    can be used in a low level call from another contract:

    ```solidity
    (bool success, bytes memory result) = router.call{value: $ethInput}(data)
    ```

    Where `$ethInput` is `0` unless the native coin of the network is an input, in which case the value
    should be set to the corresponding path input amount. Approvals for ERC20 inputs should be made to
    the router address prior to the call. The address of the router can be found in the `to` field of
    the response, as well as from the `/info/router/{version}/{chain_id}` endpoint.

    | Parameter | Description |
    | --- | --- |
    | `chainId` | The chain ID for the path to execute one |
    | `gas` | Suggested gas limit. Either 2X the naive gas estimate or 10% more than the simulated gas
    estimate |
    | `gasPrice` | Gas price used to calculate the path |
    | `value` | Input amount of gas token. 0 if the gas token is not one of the inputs |
    | `to` | Odos router address to be used for the transaction |
    | `from` | Source of the executed transaction |
    | `data` | Call data for the Odos router. This is the payload used by our executor contracts to
    execute the necessary DEX swaps. |
    | `nonce` | The standard ETH nonce |


    ### Simulation

    This the result of the simulation

    | Parameter | Description |
    | --- | --- |
    | `isSuccess` | If the transaction reverted or not |
    | `amountsOut` | Amounts out when the path was simulated |
    | `simGasUsed` | Gas used by the simulation |
    | `gasEstimate` | Estimate from a `eth_estimateGas` RPC call for the path |
    | `simulationError` | If a simulation error occurs, it will show up here. |

    Args:
        body (AssemblePathRequest): Assemble Path Request Schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PathResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AssemblePathRequest,
) -> Response[Union[Any, HTTPValidationError, PathResponse]]:
    """Assemble Odos quote into transaction

     Provide valid call data for a given quoted path. This is called after calling the `sor/quote`
    endpoint and receiving back a quote and `pathID`.

    A quote only lasts for 60 seconds. If it is not assembled in that time, it will not be available to
    assemble, and the path will need to be quoted again.

    Use the information provided by this endpoint directly. Do not try to modify the call data. You will
    make a mistake and you will end up losing money. **We will not provide support for users modifying
    the call data provided by our API.** The data the API provides is directly able to be executed on
    chain.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------- | --- |
    | `userAddr` | Address of the user who requested the quote | Yes |
    | `pathId` | ID of the Path returned from the `sor/quote/{version}` endpoint | Yes |
    | `simulate` | Simulate the transaction to make sure it can actually be executed. This increases the
    response time to receive transaction data. Defaults to False. | No |
    | `receiver` | Optionally, specify a different receiver address for the transaction output, default
    receiver is `userAddr` | No |

    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `inputTokens` | List of input token addresses and amounts |
    | `outputTokens` | List of output token addresses and amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `transaction` | Transaction data needed for execution |
    | `simulation` | Simulation results |

    ### Transaction

    This structure can be signed by a wallet and be executed against the Odos router.

    In the smart contract that makes the swap, the `data` field of the transaction given in the response
    can be used in a low level call from another contract:

    ```solidity
    (bool success, bytes memory result) = router.call{value: $ethInput}(data)
    ```

    Where `$ethInput` is `0` unless the native coin of the network is an input, in which case the value
    should be set to the corresponding path input amount. Approvals for ERC20 inputs should be made to
    the router address prior to the call. The address of the router can be found in the `to` field of
    the response, as well as from the `/info/router/{version}/{chain_id}` endpoint.

    | Parameter | Description |
    | --- | --- |
    | `chainId` | The chain ID for the path to execute one |
    | `gas` | Suggested gas limit. Either 2X the naive gas estimate or 10% more than the simulated gas
    estimate |
    | `gasPrice` | Gas price used to calculate the path |
    | `value` | Input amount of gas token. 0 if the gas token is not one of the inputs |
    | `to` | Odos router address to be used for the transaction |
    | `from` | Source of the executed transaction |
    | `data` | Call data for the Odos router. This is the payload used by our executor contracts to
    execute the necessary DEX swaps. |
    | `nonce` | The standard ETH nonce |


    ### Simulation

    This the result of the simulation

    | Parameter | Description |
    | --- | --- |
    | `isSuccess` | If the transaction reverted or not |
    | `amountsOut` | Amounts out when the path was simulated |
    | `simGasUsed` | Gas used by the simulation |
    | `gasEstimate` | Estimate from a `eth_estimateGas` RPC call for the path |
    | `simulationError` | If a simulation error occurs, it will show up here. |

    Args:
        body (AssemblePathRequest): Assemble Path Request Schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PathResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AssemblePathRequest,
) -> Optional[Union[Any, HTTPValidationError, PathResponse]]:
    """Assemble Odos quote into transaction

     Provide valid call data for a given quoted path. This is called after calling the `sor/quote`
    endpoint and receiving back a quote and `pathID`.

    A quote only lasts for 60 seconds. If it is not assembled in that time, it will not be available to
    assemble, and the path will need to be quoted again.

    Use the information provided by this endpoint directly. Do not try to modify the call data. You will
    make a mistake and you will end up losing money. **We will not provide support for users modifying
    the call data provided by our API.** The data the API provides is directly able to be executed on
    chain.

    ## Request Body

    | Parameter | Description | Required |
    | --- | ------- | --- |
    | `userAddr` | Address of the user who requested the quote | Yes |
    | `pathId` | ID of the Path returned from the `sor/quote/{version}` endpoint | Yes |
    | `simulate` | Simulate the transaction to make sure it can actually be executed. This increases the
    response time to receive transaction data. Defaults to False. | No |
    | `receiver` | Optionally, specify a different receiver address for the transaction output, default
    receiver is `userAddr` | No |

    ## Response Body

    | Parameter | Description |
    | --- | --- |
    | `deprecated` | If the endpoint or any part of the request is deprecated, this field will be
    populated with a message. This field is omitted if there is nothing to notify on. |
    | `blockNumber` | Block number the quote was generated for |
    | `gasEstimate` | A very naive gas estimate |
    | `gasEstimateValue` | USD Value of the `gasEstimate` |
    | `inputTokens` | List of input token addresses and amounts |
    | `outputTokens` | List of output token addresses and amounts |
    | `netOutValue` | USD value of the sum of the output tokens after gas |
    | `outValues` | A list of the output values of the given output tokens. In the same order as the
    `outputTokens` list |
    | `transaction` | Transaction data needed for execution |
    | `simulation` | Simulation results |

    ### Transaction

    This structure can be signed by a wallet and be executed against the Odos router.

    In the smart contract that makes the swap, the `data` field of the transaction given in the response
    can be used in a low level call from another contract:

    ```solidity
    (bool success, bytes memory result) = router.call{value: $ethInput}(data)
    ```

    Where `$ethInput` is `0` unless the native coin of the network is an input, in which case the value
    should be set to the corresponding path input amount. Approvals for ERC20 inputs should be made to
    the router address prior to the call. The address of the router can be found in the `to` field of
    the response, as well as from the `/info/router/{version}/{chain_id}` endpoint.

    | Parameter | Description |
    | --- | --- |
    | `chainId` | The chain ID for the path to execute one |
    | `gas` | Suggested gas limit. Either 2X the naive gas estimate or 10% more than the simulated gas
    estimate |
    | `gasPrice` | Gas price used to calculate the path |
    | `value` | Input amount of gas token. 0 if the gas token is not one of the inputs |
    | `to` | Odos router address to be used for the transaction |
    | `from` | Source of the executed transaction |
    | `data` | Call data for the Odos router. This is the payload used by our executor contracts to
    execute the necessary DEX swaps. |
    | `nonce` | The standard ETH nonce |


    ### Simulation

    This the result of the simulation

    | Parameter | Description |
    | --- | --- |
    | `isSuccess` | If the transaction reverted or not |
    | `amountsOut` | Amounts out when the path was simulated |
    | `simGasUsed` | Gas used by the simulation |
    | `gasEstimate` | Estimate from a `eth_estimateGas` RPC call for the path |
    | `simulationError` | If a simulation error occurs, it will show up here. |

    Args:
        body (AssemblePathRequest): Assemble Path Request Schema

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PathResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
