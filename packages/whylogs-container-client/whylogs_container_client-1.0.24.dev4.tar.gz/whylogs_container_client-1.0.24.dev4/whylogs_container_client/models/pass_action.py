from typing import Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PassAction")


@_attrs_define
class PassAction:
    """
    Attributes:
        action_type (Union[Literal['pass'], Unset]):  Default: 'pass'.
        is_action_pass (Union[Unset, bool]):  Default: True.
    """

    action_type: Union[Literal["pass"], Unset] = "pass"
    is_action_pass: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action_type = self.action_type

        is_action_pass = self.is_action_pass

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if is_action_pass is not UNSET:
            field_dict["is_action_pass"] = is_action_pass

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action_type = d.pop("action_type", UNSET)

        is_action_pass = d.pop("is_action_pass", UNSET)

        pass_action = cls(
            action_type=action_type,
            is_action_pass=is_action_pass,
        )

        pass_action.additional_properties = d
        return pass_action

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
