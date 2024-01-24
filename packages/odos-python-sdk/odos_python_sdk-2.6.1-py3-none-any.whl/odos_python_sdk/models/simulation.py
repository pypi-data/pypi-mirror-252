from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.simulation_error import SimulationError


T = TypeVar("T", bound="Simulation")


@_attrs_define
class Simulation:
    """Simulation data schema

    Attributes:
        is_success (bool): true if no errors were detected during simulation
        amountsOut (List[int]): list of amounts out from simulation
        gasEstimate (int): on-chain estimateGas raw response value
        simulationError (Optional[SimulationError]): simulation error data (if error)

        Attributes:
            is_success (bool):
            amounts_out (List[int]):
            gas_estimate (int):
            simulation_error (Union['SimulationError', None]):
    """

    is_success: bool
    amounts_out: List[int]
    gas_estimate: int
    simulation_error: Union["SimulationError", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.simulation_error import SimulationError

        is_success = self.is_success

        amounts_out = self.amounts_out

        gas_estimate = self.gas_estimate

        simulation_error: Union[Dict[str, Any], None]
        if isinstance(self.simulation_error, SimulationError):
            simulation_error = self.simulation_error.to_dict()
        else:
            simulation_error = self.simulation_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isSuccess": is_success,
                "amountsOut": amounts_out,
                "gasEstimate": gas_estimate,
                "simulationError": simulation_error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.simulation_error import SimulationError

        d = src_dict.copy()
        is_success = d.pop("isSuccess")

        amounts_out = cast(List[int], d.pop("amountsOut"))

        gas_estimate = d.pop("gasEstimate")

        def _parse_simulation_error(data: object) -> Union["SimulationError", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                simulation_error_type_0 = SimulationError.from_dict(data)

                return simulation_error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SimulationError", None], data)

        simulation_error = _parse_simulation_error(d.pop("simulationError"))

        simulation = cls(
            is_success=is_success,
            amounts_out=amounts_out,
            gas_estimate=gas_estimate,
            simulation_error=simulation_error,
        )

        simulation.additional_properties = d
        return simulation

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
