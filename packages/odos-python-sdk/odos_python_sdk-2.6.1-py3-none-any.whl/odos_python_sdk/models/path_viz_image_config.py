from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PathVizImageConfig")


@_attrs_define
class PathVizImageConfig:
    """Schema for path viz image config

    Attributes:
        link_colors (Union[List[str], None, Unset]):
        node_color (Union[None, Unset, str]):
        node_text_color (Union[None, Unset, str]):
        legend_text_color (Union[None, Unset, str]):
        width (Union[None, Unset, int]):
        height (Union[None, Unset, int]):
    """

    link_colors: Union[List[str], None, Unset] = UNSET
    node_color: Union[None, Unset, str] = UNSET
    node_text_color: Union[None, Unset, str] = UNSET
    legend_text_color: Union[None, Unset, str] = UNSET
    width: Union[None, Unset, int] = UNSET
    height: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        link_colors: Union[List[str], None, Unset]
        if isinstance(self.link_colors, Unset):
            link_colors = UNSET
        elif isinstance(self.link_colors, list):
            link_colors = self.link_colors

        else:
            link_colors = self.link_colors

        node_color: Union[None, Unset, str]
        if isinstance(self.node_color, Unset):
            node_color = UNSET
        else:
            node_color = self.node_color

        node_text_color: Union[None, Unset, str]
        if isinstance(self.node_text_color, Unset):
            node_text_color = UNSET
        else:
            node_text_color = self.node_text_color

        legend_text_color: Union[None, Unset, str]
        if isinstance(self.legend_text_color, Unset):
            legend_text_color = UNSET
        else:
            legend_text_color = self.legend_text_color

        width: Union[None, Unset, int]
        if isinstance(self.width, Unset):
            width = UNSET
        else:
            width = self.width

        height: Union[None, Unset, int]
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if link_colors is not UNSET:
            field_dict["linkColors"] = link_colors
        if node_color is not UNSET:
            field_dict["nodeColor"] = node_color
        if node_text_color is not UNSET:
            field_dict["nodeTextColor"] = node_text_color
        if legend_text_color is not UNSET:
            field_dict["legendTextColor"] = legend_text_color
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_link_colors(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                link_colors_type_0 = cast(List[str], data)

                return link_colors_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        link_colors = _parse_link_colors(d.pop("linkColors", UNSET))

        def _parse_node_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_color = _parse_node_color(d.pop("nodeColor", UNSET))

        def _parse_node_text_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_text_color = _parse_node_text_color(d.pop("nodeTextColor", UNSET))

        def _parse_legend_text_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        legend_text_color = _parse_legend_text_color(d.pop("legendTextColor", UNSET))

        def _parse_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        width = _parse_width(d.pop("width", UNSET))

        def _parse_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        height = _parse_height(d.pop("height", UNSET))

        path_viz_image_config = cls(
            link_colors=link_colors,
            node_color=node_color,
            node_text_color=node_text_color,
            legend_text_color=legend_text_color,
            width=width,
            height=height,
        )

        path_viz_image_config.additional_properties = d
        return path_viz_image_config

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
