from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_token_price_map_tokenprices import ChainTokenPriceMapTokenprices


T = TypeVar("T", bound="ChainTokenPriceMap")


@_attrs_define
class ChainTokenPriceMap:
    """All token prices for a given chain

    Attributes:
        currencyId (str): price service id of the currency
        tokenPrices (dict): Token and price

        Attributes:
            currency_id (str):
            token_prices (ChainTokenPriceMapTokenprices):
            deprecated (Union[None, Unset, str]):
    """

    currency_id: str
    token_prices: "ChainTokenPriceMapTokenprices"
    deprecated: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency_id = self.currency_id

        token_prices = self.token_prices.to_dict()

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
                "tokenPrices": token_prices,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chain_token_price_map_tokenprices import ChainTokenPriceMapTokenprices

        d = src_dict.copy()
        currency_id = d.pop("currencyId")

        token_prices = ChainTokenPriceMapTokenprices.from_dict(d.pop("tokenPrices"))

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        chain_token_price_map = cls(
            currency_id=currency_id,
            token_prices=token_prices,
            deprecated=deprecated,
        )

        chain_token_price_map.additional_properties = d
        return chain_token_price_map

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
