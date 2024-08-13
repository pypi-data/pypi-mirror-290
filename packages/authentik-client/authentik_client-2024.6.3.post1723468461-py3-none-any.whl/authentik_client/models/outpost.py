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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.outpost_type_enum import OutpostTypeEnum
from authentik_client.models.provider import Provider
from authentik_client.models.service_connection import ServiceConnection
from typing import Optional, Set
from typing_extensions import Self

class Outpost(BaseModel):
    """
    Outpost Serializer
    """ # noqa: E501
    pk: StrictStr
    name: StrictStr
    type: OutpostTypeEnum
    providers: List[StrictInt]
    providers_obj: List[Provider]
    service_connection: Optional[StrictStr] = Field(default=None, description="Select Service-Connection authentik should use to manage this outpost. Leave empty if authentik should not handle the deployment.")
    service_connection_obj: ServiceConnection
    refresh_interval_s: StrictInt
    token_identifier: StrictStr = Field(description="Get Token identifier")
    config: Dict[str, Any]
    managed: Optional[StrictStr] = Field(default=None, description="Objects that are managed by authentik. These objects are created and updated automatically. This flag only indicates that an object can be overwritten by migrations. You can still modify the objects via the API, but expect changes to be overwritten in a later update.")
    __properties: ClassVar[List[str]] = ["pk", "name", "type", "providers", "providers_obj", "service_connection", "service_connection_obj", "refresh_interval_s", "token_identifier", "config", "managed"]

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
        """Create an instance of Outpost from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "pk",
            "providers_obj",
            "service_connection_obj",
            "refresh_interval_s",
            "token_identifier",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in providers_obj (list)
        _items = []
        if self.providers_obj:
            for _item in self.providers_obj:
                if _item:
                    _items.append(_item.to_dict())
            _dict['providers_obj'] = _items
        # override the default output from pydantic by calling `to_dict()` of service_connection_obj
        if self.service_connection_obj:
            _dict['service_connection_obj'] = self.service_connection_obj.to_dict()
        # set to None if service_connection (nullable) is None
        # and model_fields_set contains the field
        if self.service_connection is None and "service_connection" in self.model_fields_set:
            _dict['service_connection'] = None

        # set to None if managed (nullable) is None
        # and model_fields_set contains the field
        if self.managed is None and "managed" in self.model_fields_set:
            _dict['managed'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Outpost from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pk": obj.get("pk"),
            "name": obj.get("name"),
            "type": obj.get("type"),
            "providers": obj.get("providers"),
            "providers_obj": [Provider.from_dict(_item) for _item in obj["providers_obj"]] if obj.get("providers_obj") is not None else None,
            "service_connection": obj.get("service_connection"),
            "service_connection_obj": ServiceConnection.from_dict(obj["service_connection_obj"]) if obj.get("service_connection_obj") is not None else None,
            "refresh_interval_s": obj.get("refresh_interval_s"),
            "token_identifier": obj.get("token_identifier"),
            "config": obj.get("config"),
            "managed": obj.get("managed")
        })
        return _obj


