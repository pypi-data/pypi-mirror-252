from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenPrice")


@_attrs_define
class TokenPrice:
    """Schema for basic token price structure

    Attributes:
        currencyId (str): price service id of the currency
        price (Optional[float]): fiat price of asset if it is available

        Attributes:
            currency_id (str):
            price (Union[None, float]):
            deprecated (Union[None, Unset, str]):
    """

    currency_id: str
    price: Union[None, float]
    deprecated: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency_id = self.currency_id

        price: Union[None, float]
        price = self.price

        deprecated: Union[None, Unset, str]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currencyId": currency_id,
                "price": price,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency_id = d.pop("currencyId")

        def _parse_price(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        price = _parse_price(d.pop("price"))

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        token_price = cls(
            currency_id=currency_id,
            price=price,
            deprecated=deprecated,
        )

        token_price.additional_properties = d
        return token_price

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
