# coding: utf-8

"""
    authentik

    Making authentication simple.

    The version of the OpenAPI document: 2024.6.3
    Contact: hello@goauthentik.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.prompt_type_enum import PromptTypeEnum
from authentik_client.models.stage_request import StageRequest
from typing import Optional, Set
from typing_extensions import Self

class PatchedPromptRequest(BaseModel):
    """
    Prompt Serializer
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    field_key: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Name of the form field, also used to store the value")
    label: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    type: Optional[PromptTypeEnum] = None
    required: Optional[StrictBool] = None
    placeholder: Optional[StrictStr] = Field(default=None, description="Optionally provide a short hint that describes the expected input value. When creating a fixed choice field, enable interpreting as expression and return a list to return multiple choices.")
    initial_value: Optional[StrictStr] = Field(default=None, description="Optionally pre-fill the input with an initial value. When creating a fixed choice field, enable interpreting as expression and return a list to return multiple default choices.")
    order: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=-2147483648)]] = None
    promptstage_set: Optional[List[StageRequest]] = None
    sub_text: Optional[StrictStr] = None
    placeholder_expression: Optional[StrictBool] = None
    initial_value_expression: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["name", "field_key", "label", "type", "required", "placeholder", "initial_value", "order", "promptstage_set", "sub_text", "placeholder_expression", "initial_value_expression"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of PatchedPromptRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in promptstage_set (list)
        _items = []
        if self.promptstage_set:
            for _item in self.promptstage_set:
                if _item:
                    _items.append(_item.to_dict())
            _dict['promptstage_set'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchedPromptRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "field_key": obj.get("field_key"),
            "label": obj.get("label"),
            "type": obj.get("type"),
            "required": obj.get("required"),
            "placeholder": obj.get("placeholder"),
            "initial_value": obj.get("initial_value"),
            "order": obj.get("order"),
            "promptstage_set": [StageRequest.from_dict(_item) for _item in obj["promptstage_set"]] if obj.get("promptstage_set") is not None else None,
            "sub_text": obj.get("sub_text"),
            "placeholder_expression": obj.get("placeholder_expression"),
            "initial_value_expression": obj.get("initial_value_expression")
        })
        return _obj


