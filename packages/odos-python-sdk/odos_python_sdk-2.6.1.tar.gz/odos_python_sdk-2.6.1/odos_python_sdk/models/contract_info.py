from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contract_info_erc_20_abi_type_0 import ContractInfoErc20AbiType0
    from ..models.contract_info_router_abi_type_0 import ContractInfoRouterAbiType0


T = TypeVar("T", bound="ContractInfo")


@_attrs_define
class ContractInfo:
    """Odos Contract Info Schema

    Attributes:
        chain_id (int):
        router_address (str):
        executor_address (str):
        router_abi (Union['ContractInfoRouterAbiType0', None]):
        erc_20_abi (Union['ContractInfoErc20AbiType0', None]):
        deprecated (Union[None, Unset, str]):
    """

    chain_id: int
    router_address: str
    executor_address: str
    router_abi: Union["ContractInfoRouterAbiType0", None]
    erc_20_abi: Union["ContractInfoErc20AbiType0", None]
    deprecated: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.contract_info_erc_20_abi_type_0 import ContractInfoErc20AbiType0
        from ..models.contract_info_router_abi_type_0 import ContractInfoRouterAbiType0

        chain_id = self.chain_id

        router_address = self.router_address

        executor_address = self.executor_address

        router_abi: Union[Dict[str, Any], None]
        if isinstance(self.router_abi, ContractInfoRouterAbiType0):
            router_abi = self.router_abi.to_dict()
        else:
            router_abi = self.router_abi

        erc_20_abi: Union[Dict[str, Any], None]
        if isinstance(self.erc_20_abi, ContractInfoErc20AbiType0):
            erc_20_abi = self.erc_20_abi.to_dict()
        else:
            erc_20_abi = self.erc_20_abi

        deprecated: Union[None, Unset, str]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chainId": chain_id,
                "routerAddress": router_address,
                "executorAddress": executor_address,
                "routerAbi": router_abi,
                "erc20Abi": erc_20_abi,
            }
        )
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.contract_info_erc_20_abi_type_0 import ContractInfoErc20AbiType0
        from ..models.contract_info_router_abi_type_0 import ContractInfoRouterAbiType0

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        router_address = d.pop("routerAddress")

        executor_address = d.pop("executorAddress")

        def _parse_router_abi(data: object) -> Union["ContractInfoRouterAbiType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                router_abi_type_0 = ContractInfoRouterAbiType0.from_dict(data)

                return router_abi_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ContractInfoRouterAbiType0", None], data)

        router_abi = _parse_router_abi(d.pop("routerAbi"))

        def _parse_erc_20_abi(data: object) -> Union["ContractInfoErc20AbiType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                erc_20_abi_type_0 = ContractInfoErc20AbiType0.from_dict(data)

                return erc_20_abi_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ContractInfoErc20AbiType0", None], data)

        erc_20_abi = _parse_erc_20_abi(d.pop("erc20Abi"))

        def _parse_deprecated(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        contract_info = cls(
            chain_id=chain_id,
            router_address=router_address,
            executor_address=executor_address,
            router_abi=router_abi,
            erc_20_abi=erc_20_abi,
            deprecated=deprecated,
        )

        contract_info.additional_properties = d
        return contract_info

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
