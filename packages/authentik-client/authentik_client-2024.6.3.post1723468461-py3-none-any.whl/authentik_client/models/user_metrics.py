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

from pydantic import BaseModel, ConfigDict
from typing import Any, ClassVar, Dict, List
from authentik_client.models.coordinate import Coordinate
from typing import Optional, Set
from typing_extensions import Self

class UserMetrics(BaseModel):
    """
    User Metrics
    """ # noqa: E501
    logins: List[Coordinate]
    logins_failed: List[Coordinate]
    authorizations: List[Coordinate]
    __properties: ClassVar[List[str]] = ["logins", "logins_failed", "authorizations"]

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
        """Create an instance of UserMetrics from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "logins",
            "logins_failed",
            "authorizations",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in logins (list)
        _items = []
        if self.logins:
            for _item in self.logins:
                if _item:
                    _items.append(_item.to_dict())
            _dict['logins'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in logins_failed (list)
        _items = []
        if self.logins_failed:
            for _item in self.logins_failed:
                if _item:
                    _items.append(_item.to_dict())
            _dict['logins_failed'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in authorizations (list)
        _items = []
        if self.authorizations:
            for _item in self.authorizations:
                if _item:
                    _items.append(_item.to_dict())
            _dict['authorizations'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserMetrics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "logins": [Coordinate.from_dict(_item) for _item in obj["logins"]] if obj.get("logins") is not None else None,
            "logins_failed": [Coordinate.from_dict(_item) for _item in obj["logins_failed"]] if obj.get("logins_failed") is not None else None,
            "authorizations": [Coordinate.from_dict(_item) for _item in obj["authorizations"]] if obj.get("authorizations") is not None else None
        })
        return _obj


