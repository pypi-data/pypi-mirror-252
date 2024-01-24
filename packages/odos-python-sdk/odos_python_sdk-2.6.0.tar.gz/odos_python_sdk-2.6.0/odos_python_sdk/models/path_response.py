from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.simulation import Simulation
    from ..models.token_amount import TokenAmount
    from ..models.transaction import Transaction


T = TypeVar("T", bound="PathResponse")


@_attrs_define
class PathResponse:
    """Assembled Path Transaction Response including quote, transaction, and simulation data

    Attributes:
        blockNumber (int): block number of transaction quote
        gasEstimate (int): gas estimate for transaction quote
        gasEstimateValue (float): gas estimate value for transaction quote in gwei
        inputTokens (List[TokenAmount]): list of input token amounts and input values
        outputTokens (List[TokenAmount]): list of output token amounts and output values
        netOutValue (float): new out value of transaction from quote
        outValues (List[str]) out values from transaction quote
        transaction (Optional[Transaction]): assembled transaction data for quote
        simulation (Optional[Simulation]): simulation output data if enabled
        pathVizImage (Optional[str]): path viz image if requested

        Attributes:
            block_number (int):
            gas_estimate (int):
            gas_estimate_value (float):
            input_tokens (List['TokenAmount']):
            output_tokens (List['TokenAmount']):
            net_out_value (float):
            out_values (List[str]):
            transaction (Union['Transaction', None]):
            simulation (Union['Simulation', None]):
            deprecated (Union[None, Unset, str]):
    """

    block_number: int
    gas_estimate: int
    gas_estimate_value: float
    input_tokens: List["TokenAmount"]
    output_tokens: List["TokenAmount"]
    net_out_value: float
    out_values: List[str]
    transaction: Union["Transaction", None]
    simulation: Union["Simulation", None]
    deprecated: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.simulation import Simulation
        from ..models.transaction import Transaction

        block_number = self.block_number

        gas_estimate = self.gas_estimate

        gas_estimate_value = self.gas_estimate_value

        input_tokens = []
        for input_tokens_item_data in self.input_tokens:
            input_tokens_item = input_tokens_item_data.to_dict()
            input_tokens.append(input_tokens_item)

        output_tokens = []
        for output_tokens_item_data in self.output_tokens:
            output_tokens_item = output_tokens_item_data.to_dict()
            output_tokens.append(output_tokens_item)

        net_out_value = self.net_out_value

        out_values = self.out_values

        transaction: Union[Dict[str, Any], None]
        if isinstance(self.transaction, Transaction):
            transaction = self.transaction.to_dict()
        else:
            transaction = self.transaction

        simulation: Union[Dict[str, Any], None]
        if isinstance(self.simulation, Simulation):
            simulation = self.simulation.to_dict()
        else:
            simulation = self.simulation

        deprecated: Union[None, Unset, str]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blockNumber": block_number,
                "gasEstimate": gas_estimate,
                "gasEstimateValue": gas_estimate_value,
                "inputTokens": input_tokens,
                "outputTokens": output_tokens,
                "netOutValue": net_out_value,
                "outValues": out_values,
                "transaction": transaction,
                "simulation": simulation,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.simulation import Simulation
        from ..models.token_amount import TokenAmount
        from ..models.transaction import Transaction

        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        gas_estimate = d.pop("gasEstimate")

        gas_estimate_value = d.pop("gasEstimateValue")

        input_tokens = []
        _input_tokens = d.pop("inputTokens")
        for input_tokens_item_data in _input_tokens:
            input_tokens_item = TokenAmount.from_dict(input_tokens_item_data)

            input_tokens.append(input_tokens_item)

        output_tokens = []
        _output_tokens = d.pop("outputTokens")
        for output_tokens_item_data in _output_tokens:
            output_tokens_item = TokenAmount.from_dict(output_tokens_item_data)

            output_tokens.append(output_tokens_item)

        net_out_value = d.pop("netOutValue")

        out_values = cast(List[str], d.pop("outValues"))

        def _parse_transaction(data: object) -> Union["Transaction", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                transaction_type_0 = Transaction.from_dict(data)

                return transaction_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Transaction", None], data)

        transaction = _parse_transaction(d.pop("transaction"))

        def _parse_simulation(data: object) -> Union["Simulation", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                simulation_type_0 = Simulation.from_dict(data)

                return simulation_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Simulation", None], data)

        simulation = _parse_simulation(d.pop("simulation"))

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        path_response = cls(
            block_number=block_number,
            gas_estimate=gas_estimate,
            gas_estimate_value=gas_estimate_value,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            net_out_value=net_out_value,
            out_values=out_values,
            transaction=transaction,
            simulation=simulation,
            deprecated=deprecated,
        )

        path_response.additional_properties = d
        return path_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
