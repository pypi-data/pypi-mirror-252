from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Token")


@_attrs_define
class Token:
    """Token Schema

    Attributes:
        name (str):
        symbol (str):
        decimals (int):
        asset_id (str):
        asset_type (str):
        protocol_id (Union[None, str]):
        is_rebasing (bool):
    """

    name: str
    symbol: str
    decimals: int
    asset_id: str
    asset_type: str
    protocol_id: Union[None, str]
    is_rebasing: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        symbol = self.symbol

        decimals = self.decimals

        asset_id = self.asset_id

        asset_type = self.asset_type

        protocol_id: Union[None, str]
        protocol_id = self.protocol_id

        is_rebasing = self.is_rebasing

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "symbol": symbol,
                "decimals": decimals,
                "assetId": asset_id,
                "assetType": asset_type,
                "protocolId": protocol_id,
                "isRebasing": is_rebasing,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        symbol = d.pop("symbol")

        decimals = d.pop("decimals")

        asset_id = d.pop("assetId")

        asset_type = d.pop("assetType")

        def _parse_protocol_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        protocol_id = _parse_protocol_id(d.pop("protocolId"))

        is_rebasing = d.pop("isRebasing")

        token = cls(
            name=name,
            symbol=symbol,
            decimals=decimals,
            asset_id=asset_id,
            asset_type=asset_type,
            protocol_id=protocol_id,
            is_rebasing=is_rebasing,
        )

        token.additional_properties = d
        return token

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
