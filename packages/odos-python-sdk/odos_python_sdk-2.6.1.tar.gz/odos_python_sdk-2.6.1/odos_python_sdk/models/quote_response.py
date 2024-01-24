from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.quote_response_path_viz_type_0 import QuoteResponsePathVizType0


T = TypeVar("T", bound="QuoteResponse")


@_attrs_define
class QuoteResponse:
    """Quote response schema

    Attributes:
        in_tokens (List[str]):
        out_tokens (List[str]):
        in_amounts (List[str]):
        out_amounts (List[str]):
        gas_estimate (float):
        data_gas_estimate (int):
        gwei_per_gas (float):
        gas_estimate_value (float):
        in_values (List[float]):
        out_values (List[float]):
        net_out_value (float):
        percent_diff (float):
        block_number (int):
        deprecated (Union[None, Unset, str]):
        price_impact (Union[None, Unset, float]):
        partner_fee_percent (Union[Unset, float]):  Default: 0.0.
        path_id (Union[None, Unset, str]):
        path_viz (Union['QuoteResponsePathVizType0', None, Unset]):
        path_viz_image (Union[None, Unset, str]):
    """

    in_tokens: List[str]
    out_tokens: List[str]
    in_amounts: List[str]
    out_amounts: List[str]
    gas_estimate: float
    data_gas_estimate: int
    gwei_per_gas: float
    gas_estimate_value: float
    in_values: List[float]
    out_values: List[float]
    net_out_value: float
    percent_diff: float
    block_number: int
    deprecated: Union[None, Unset, str] = UNSET
    price_impact: Union[None, Unset, float] = UNSET
    partner_fee_percent: Union[Unset, float] = 0.0
    path_id: Union[None, Unset, str] = UNSET
    path_viz: Union["QuoteResponsePathVizType0", None, Unset] = UNSET
    path_viz_image: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.quote_response_path_viz_type_0 import QuoteResponsePathVizType0

        in_tokens = self.in_tokens

        out_tokens = self.out_tokens

        in_amounts = self.in_amounts

        out_amounts = self.out_amounts

        gas_estimate = self.gas_estimate

        data_gas_estimate = self.data_gas_estimate

        gwei_per_gas = self.gwei_per_gas

        gas_estimate_value = self.gas_estimate_value

        in_values = self.in_values

        out_values = self.out_values

        net_out_value = self.net_out_value

        percent_diff = self.percent_diff

        block_number = self.block_number

        deprecated: Union[None, Unset, str]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        price_impact: Union[None, Unset, float]
        if isinstance(self.price_impact, Unset):
            price_impact = UNSET
        else:
            price_impact = self.price_impact

        partner_fee_percent = self.partner_fee_percent

        path_id: Union[None, Unset, str]
        if isinstance(self.path_id, Unset):
            path_id = UNSET
        else:
            path_id = self.path_id

        path_viz: Union[Dict[str, Any], None, Unset]
        if isinstance(self.path_viz, Unset):
            path_viz = UNSET
        elif isinstance(self.path_viz, QuoteResponsePathVizType0):
            path_viz = self.path_viz.to_dict()
        else:
            path_viz = self.path_viz

        path_viz_image: Union[None, Unset, str]
        if isinstance(self.path_viz_image, Unset):
            path_viz_image = UNSET
        else:
            path_viz_image = self.path_viz_image

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inTokens": in_tokens,
                "outTokens": out_tokens,
                "inAmounts": in_amounts,
                "outAmounts": out_amounts,
                "gasEstimate": gas_estimate,
                "dataGasEstimate": data_gas_estimate,
                "gweiPerGas": gwei_per_gas,
                "gasEstimateValue": gas_estimate_value,
                "inValues": in_values,
                "outValues": out_values,
                "netOutValue": net_out_value,
                "percentDiff": percent_diff,
                "blockNumber": block_number,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if price_impact is not UNSET:
            field_dict["priceImpact"] = price_impact
        if partner_fee_percent is not UNSET:
            field_dict["partnerFeePercent"] = partner_fee_percent
        if path_id is not UNSET:
            field_dict["pathId"] = path_id
        if path_viz is not UNSET:
            field_dict["pathViz"] = path_viz
        if path_viz_image is not UNSET:
            field_dict["pathVizImage"] = path_viz_image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.quote_response_path_viz_type_0 import QuoteResponsePathVizType0

        d = src_dict.copy()
        in_tokens = cast(List[str], d.pop("inTokens"))

        out_tokens = cast(List[str], d.pop("outTokens"))

        in_amounts = cast(List[str], d.pop("inAmounts"))

        out_amounts = cast(List[str], d.pop("outAmounts"))

        gas_estimate = d.pop("gasEstimate")

        data_gas_estimate = d.pop("dataGasEstimate")

        gwei_per_gas = d.pop("gweiPerGas")

        gas_estimate_value = d.pop("gasEstimateValue")

        in_values = cast(List[float], d.pop("inValues"))

        out_values = cast(List[float], d.pop("outValues"))

        net_out_value = d.pop("netOutValue")

        percent_diff = d.pop("percentDiff")

        block_number = d.pop("blockNumber")

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        def _parse_price_impact(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        price_impact = _parse_price_impact(d.pop("priceImpact", UNSET))

        partner_fee_percent = d.pop("partnerFeePercent", UNSET)

        def _parse_path_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        path_id = _parse_path_id(d.pop("pathId", UNSET))

        def _parse_path_viz(data: object) -> Union["QuoteResponsePathVizType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                path_viz_type_0 = QuoteResponsePathVizType0.from_dict(data)

                return path_viz_type_0
            except:  # noqa: E722
                pass
            return cast(Union["QuoteResponsePathVizType0", None, Unset], data)

        path_viz = _parse_path_viz(d.pop("pathViz", UNSET))

        def _parse_path_viz_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        path_viz_image = _parse_path_viz_image(d.pop("pathVizImage", UNSET))

        quote_response = cls(
            in_tokens=in_tokens,
            out_tokens=out_tokens,
            in_amounts=in_amounts,
            out_amounts=out_amounts,
            gas_estimate=gas_estimate,
            data_gas_estimate=data_gas_estimate,
            gwei_per_gas=gwei_per_gas,
            gas_estimate_value=gas_estimate_value,
            in_values=in_values,
            out_values=out_values,
            net_out_value=net_out_value,
            percent_diff=percent_diff,
            block_number=block_number,
            deprecated=deprecated,
            price_impact=price_impact,
            partner_fee_percent=partner_fee_percent,
            path_id=path_id,
            path_viz=path_viz,
            path_viz_image=path_viz_image,
        )

        quote_response.additional_properties = d
        return quote_response

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
