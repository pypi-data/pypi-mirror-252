from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """Assembled Transaction Schema

    Attributes:
        gas (int): txn gas amount
        gasPrice (int): txn gas price in gwei
        value (str): value of the transaction
        to (str): txn to address
        from_ (str): txn from address
        data (str): txn bytecode to execute
        nonce (int): current user nonce
        chainId (int): id of the chain transaction was assembled for

        Attributes:
            gas (int):
            gas_price (int):
            value (str):
            to (str):
            from_ (str):
            data (str):
            nonce (int):
            chain_id (int):
    """

    gas: int
    gas_price: int
    value: str
    to: str
    from_: str
    data: str
    nonce: int
    chain_id: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gas = self.gas

        gas_price = self.gas_price

        value = self.value

        to = self.to

        from_ = self.from_

        data = self.data

        nonce = self.nonce

        chain_id = self.chain_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gas": gas,
                "gasPrice": gas_price,
                "value": value,
                "to": to,
                "from": from_,
                "data": data,
                "nonce": nonce,
                "chainId": chain_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        gas = d.pop("gas")

        gas_price = d.pop("gasPrice")

        value = d.pop("value")

        to = d.pop("to")

        from_ = d.pop("from")

        data = d.pop("data")

        nonce = d.pop("nonce")

        chain_id = d.pop("chainId")

        transaction = cls(
            gas=gas,
            gas_price=gas_price,
            value=value,
            to=to,
            from_=from_,
            data=data,
            nonce=nonce,
            chain_id=chain_id,
        )

        transaction.additional_properties = d
        return transaction

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
