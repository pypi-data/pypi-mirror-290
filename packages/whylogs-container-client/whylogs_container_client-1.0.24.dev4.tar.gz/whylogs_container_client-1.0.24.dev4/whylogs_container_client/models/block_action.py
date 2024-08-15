from typing import Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlockAction")


@_attrs_define
class BlockAction:
    """
    Attributes:
        block_message (str):
        action_type (Union[Literal['block'], Unset]):  Default: 'block'.
        is_action_block (Union[Unset, bool]):  Default: True.
    """

    block_message: str
    action_type: Union[Literal["block"], Unset] = "block"
    is_action_block: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        block_message = self.block_message

        action_type = self.action_type

        is_action_block = self.is_action_block

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "block_message": block_message,
            }
        )
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if is_action_block is not UNSET:
            field_dict["is_action_block"] = is_action_block

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_message = d.pop("block_message")

        action_type = d.pop("action_type", UNSET)

        is_action_block = d.pop("is_action_block", UNSET)

        block_action = cls(
            block_message=block_message,
            action_type=action_type,
            is_action_block=is_action_block,
        )

        block_action.additional_properties = d
        return block_action

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
