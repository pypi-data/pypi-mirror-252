from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.currency_info import CurrencyInfo


T = TypeVar("T", bound="CurrencyInfoList")


@_attrs_define
class CurrencyInfoList:
    """Schema for list of supported currency info

    Attributes:
        currencies (List[CurrencyInfo]): list of supported currency info entries

        Attributes:
            currencies (List['CurrencyInfo']):
            deprecated (Union[None, Unset, str]):
    """

    currencies: List["CurrencyInfo"]
    deprecated: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currencies = []
        for currencies_item_data in self.currencies:
            currencies_item = currencies_item_data.to_dict()
            currencies.append(currencies_item)

        deprecated: Union[None, Unset, str]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currencies": currencies,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.currency_info import CurrencyInfo

        d = src_dict.copy()
        currencies = []
        _currencies = d.pop("currencies")
        for currencies_item_data in _currencies:
            currencies_item = CurrencyInfo.from_dict(currencies_item_data)

            currencies.append(currencies_item)

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        currency_info_list = cls(
            currencies=currencies,
            deprecated=deprecated,
        )

        currency_info_list.additional_properties = d
        return currency_info_list

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
