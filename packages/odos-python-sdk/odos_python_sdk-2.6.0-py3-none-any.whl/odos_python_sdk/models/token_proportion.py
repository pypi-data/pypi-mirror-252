from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenProportion")


@_attrs_define
class TokenProportion:
    """Quote token output proportion schema

    Attributes:
        token_address (str): Token contract address
        proportion (Union[Unset, float]): Proportion of token Default: 1.0.
    """

    token_address: str
    proportion: Union[Unset, float] = 1.0
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token_address = self.token_address

        proportion = self.proportion

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tokenAddress": token_address,
            }
        )
        if proportion is not UNSET:
            field_dict["proportion"] = proportion

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token_address = d.pop("tokenAddress")

        proportion = d.pop("proportion", UNSET)

        token_proportion = cls(
            token_address=token_address,
            proportion=proportion,
        )

        token_proportion.additional_properties = d
        return token_proportion

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
