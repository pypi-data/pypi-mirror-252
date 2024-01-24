from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.path_viz_image_config import PathVizImageConfig
    from ..models.token_amount import TokenAmount
    from ..models.token_proportion import TokenProportion


T = TypeVar("T", bound="PathRequestV2")


@_attrs_define
class PathRequestV2:
    """Public facing path request v2 schema

    Attributes:
        chain_id (int): Chain ID to request path for
        input_tokens (List['TokenAmount']): Input tokens and amounts for quote
        output_tokens (List['TokenProportion']): Output tokens and proportions for quote
        deprecated (Union[None, Unset, str]):
        gas_price (Union[None, Unset, float]): Gas Price
        user_addr (Union[None, Unset, str]): Address of wallet to use to generate transaction Default:
            '0x47E2D28169738039755586743E2dfCF3bd643f86'.
        slippage_limit_percent (Union[None, Unset, float]): Slippage to use for checking the path is valid Default: 0.3.
        source_blacklist (Union[List[str], None, Unset]): List of liquidity providers that are not to be used for the
            swap path.
        source_whitelist (Union[List[str], None, Unset]): List of liquidity providers to exclusively use for the swap
            path.
        path_viz (Union[None, Unset, bool]):  Default: False.
        path_viz_image (Union[None, Unset, bool]):  Default: False.
        path_viz_image_config (Union['PathVizImageConfig', None, Unset]):
        disable_rf_qs (Union[None, Unset, bool]): Flag to disable all off-chain RFQs from order routing Default: True.
        referral_code (Union[None, Unset, int]):  Default: 0.
        compact (Union[None, Unset, bool]):  Default: True.
        like_asset (Union[None, Unset, bool]):  Default: False.
        simple (Union[None, Unset, bool]):  Default: False.
    """

    chain_id: int
    input_tokens: List["TokenAmount"]
    output_tokens: List["TokenProportion"]
    deprecated: Union[None, Unset, str] = UNSET
    gas_price: Union[None, Unset, float] = UNSET
    user_addr: Union[None, Unset, str] = "0x47E2D28169738039755586743E2dfCF3bd643f86"
    slippage_limit_percent: Union[None, Unset, float] = 0.3
    source_blacklist: Union[List[str], None, Unset] = UNSET
    source_whitelist: Union[List[str], None, Unset] = UNSET
    path_viz: Union[None, Unset, bool] = False
    path_viz_image: Union[None, Unset, bool] = False
    path_viz_image_config: Union["PathVizImageConfig", None, Unset] = UNSET
    disable_rf_qs: Union[None, Unset, bool] = True
    referral_code: Union[None, Unset, int] = 0
    compact: Union[None, Unset, bool] = True
    like_asset: Union[None, Unset, bool] = False
    simple: Union[None, Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.path_viz_image_config import PathVizImageConfig

        chain_id = self.chain_id

        input_tokens = []
        for input_tokens_item_data in self.input_tokens:
            input_tokens_item = input_tokens_item_data.to_dict()
            input_tokens.append(input_tokens_item)

        output_tokens = []
        for output_tokens_item_data in self.output_tokens:
            output_tokens_item = output_tokens_item_data.to_dict()
            output_tokens.append(output_tokens_item)

        deprecated: Union[None, Unset, str]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        gas_price: Union[None, Unset, float]
        if isinstance(self.gas_price, Unset):
            gas_price = UNSET
        else:
            gas_price = self.gas_price

        user_addr: Union[None, Unset, str]
        if isinstance(self.user_addr, Unset):
            user_addr = UNSET
        else:
            user_addr = self.user_addr

        slippage_limit_percent: Union[None, Unset, float]
        if isinstance(self.slippage_limit_percent, Unset):
            slippage_limit_percent = UNSET
        else:
            slippage_limit_percent = self.slippage_limit_percent

        source_blacklist: Union[List[str], None, Unset]
        if isinstance(self.source_blacklist, Unset):
            source_blacklist = UNSET
        elif isinstance(self.source_blacklist, list):
            source_blacklist = self.source_blacklist

        else:
            source_blacklist = self.source_blacklist

        source_whitelist: Union[List[str], None, Unset]
        if isinstance(self.source_whitelist, Unset):
            source_whitelist = UNSET
        elif isinstance(self.source_whitelist, list):
            source_whitelist = self.source_whitelist

        else:
            source_whitelist = self.source_whitelist

        path_viz: Union[None, Unset, bool]
        if isinstance(self.path_viz, Unset):
            path_viz = UNSET
        else:
            path_viz = self.path_viz

        path_viz_image: Union[None, Unset, bool]
        if isinstance(self.path_viz_image, Unset):
            path_viz_image = UNSET
        else:
            path_viz_image = self.path_viz_image

        path_viz_image_config: Union[Dict[str, Any], None, Unset]
        if isinstance(self.path_viz_image_config, Unset):
            path_viz_image_config = UNSET
        elif isinstance(self.path_viz_image_config, PathVizImageConfig):
            path_viz_image_config = self.path_viz_image_config.to_dict()
        else:
            path_viz_image_config = self.path_viz_image_config

        disable_rf_qs: Union[None, Unset, bool]
        if isinstance(self.disable_rf_qs, Unset):
            disable_rf_qs = UNSET
        else:
            disable_rf_qs = self.disable_rf_qs

        referral_code: Union[None, Unset, int]
        if isinstance(self.referral_code, Unset):
            referral_code = UNSET
        else:
            referral_code = self.referral_code

        compact: Union[None, Unset, bool]
        if isinstance(self.compact, Unset):
            compact = UNSET
        else:
            compact = self.compact

        like_asset: Union[None, Unset, bool]
        if isinstance(self.like_asset, Unset):
            like_asset = UNSET
        else:
            like_asset = self.like_asset

        simple: Union[None, Unset, bool]
        if isinstance(self.simple, Unset):
            simple = UNSET
        else:
            simple = self.simple

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chainId": chain_id,
                "inputTokens": input_tokens,
                "outputTokens": output_tokens,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if gas_price is not UNSET:
            field_dict["gasPrice"] = gas_price
        if user_addr is not UNSET:
            field_dict["userAddr"] = user_addr
        if slippage_limit_percent is not UNSET:
            field_dict["slippageLimitPercent"] = slippage_limit_percent
        if source_blacklist is not UNSET:
            field_dict["sourceBlacklist"] = source_blacklist
        if source_whitelist is not UNSET:
            field_dict["sourceWhitelist"] = source_whitelist
        if path_viz is not UNSET:
            field_dict["pathViz"] = path_viz
        if path_viz_image is not UNSET:
            field_dict["pathVizImage"] = path_viz_image
        if path_viz_image_config is not UNSET:
            field_dict["pathVizImageConfig"] = path_viz_image_config
        if disable_rf_qs is not UNSET:
            field_dict["disableRFQs"] = disable_rf_qs
        if referral_code is not UNSET:
            field_dict["referralCode"] = referral_code
        if compact is not UNSET:
            field_dict["compact"] = compact
        if like_asset is not UNSET:
            field_dict["likeAsset"] = like_asset
        if simple is not UNSET:
            field_dict["simple"] = simple

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.path_viz_image_config import PathVizImageConfig
        from ..models.token_amount import TokenAmount
        from ..models.token_proportion import TokenProportion

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        input_tokens = []
        _input_tokens = d.pop("inputTokens")
        for input_tokens_item_data in _input_tokens:
            input_tokens_item = TokenAmount.from_dict(input_tokens_item_data)

            input_tokens.append(input_tokens_item)

        output_tokens = []
        _output_tokens = d.pop("outputTokens")
        for output_tokens_item_data in _output_tokens:
            output_tokens_item = TokenProportion.from_dict(output_tokens_item_data)

            output_tokens.append(output_tokens_item)

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        def _parse_gas_price(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        gas_price = _parse_gas_price(d.pop("gasPrice", UNSET))

        def _parse_user_addr(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_addr = _parse_user_addr(d.pop("userAddr", UNSET))

        def _parse_slippage_limit_percent(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        slippage_limit_percent = _parse_slippage_limit_percent(d.pop("slippageLimitPercent", UNSET))

        def _parse_source_blacklist(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_blacklist_type_0 = cast(List[str], data)

                return source_blacklist_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        source_blacklist = _parse_source_blacklist(d.pop("sourceBlacklist", UNSET))

        def _parse_source_whitelist(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_whitelist_type_0 = cast(List[str], data)

                return source_whitelist_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        source_whitelist = _parse_source_whitelist(d.pop("sourceWhitelist", UNSET))

        def _parse_path_viz(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        path_viz = _parse_path_viz(d.pop("pathViz", UNSET))

        def _parse_path_viz_image(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        path_viz_image = _parse_path_viz_image(d.pop("pathVizImage", UNSET))

        def _parse_path_viz_image_config(data: object) -> Union["PathVizImageConfig", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                path_viz_image_config_type_0 = PathVizImageConfig.from_dict(data)

                return path_viz_image_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PathVizImageConfig", None, Unset], data)

        path_viz_image_config = _parse_path_viz_image_config(d.pop("pathVizImageConfig", UNSET))

        def _parse_disable_rf_qs(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        disable_rf_qs = _parse_disable_rf_qs(d.pop("disableRFQs", UNSET))

        def _parse_referral_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        referral_code = _parse_referral_code(d.pop("referralCode", UNSET))

        def _parse_compact(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        compact = _parse_compact(d.pop("compact", UNSET))

        def _parse_like_asset(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        like_asset = _parse_like_asset(d.pop("likeAsset", UNSET))

        def _parse_simple(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        simple = _parse_simple(d.pop("simple", UNSET))

        path_request_v2 = cls(
            chain_id=chain_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            deprecated=deprecated,
            gas_price=gas_price,
            user_addr=user_addr,
            slippage_limit_percent=slippage_limit_percent,
            source_blacklist=source_blacklist,
            source_whitelist=source_whitelist,
            path_viz=path_viz,
            path_viz_image=path_viz_image,
            path_viz_image_config=path_viz_image_config,
            disable_rf_qs=disable_rf_qs,
            referral_code=referral_code,
            compact=compact,
            like_asset=like_asset,
            simple=simple,
        )

        path_request_v2.additional_properties = d
        return path_request_v2

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
