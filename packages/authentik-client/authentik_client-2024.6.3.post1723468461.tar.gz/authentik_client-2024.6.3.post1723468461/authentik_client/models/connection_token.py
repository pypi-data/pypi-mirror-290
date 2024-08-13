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

from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.endpoint import Endpoint
from authentik_client.models.group_member import GroupMember
from authentik_client.models.rac_provider import RACProvider
from typing import Optional, Set
from typing_extensions import Self

class ConnectionToken(BaseModel):
    """
    ConnectionToken Serializer
    """ # noqa: E501
    pk: Optional[StrictStr] = None
    provider: StrictInt
    provider_obj: RACProvider
    endpoint: StrictStr
    endpoint_obj: Endpoint
    user: GroupMember
    __properties: ClassVar[List[str]] = ["pk", "provider", "provider_obj", "endpoint", "endpoint_obj", "user"]

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
        """Create an instance of ConnectionToken from a JSON string"""
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
            "provider_obj",
            "endpoint_obj",
            "user",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of provider_obj
        if self.provider_obj:
            _dict['provider_obj'] = self.provider_obj.to_dict()
        # override the default output from pydantic by calling `to_dict()` of endpoint_obj
        if self.endpoint_obj:
            _dict['endpoint_obj'] = self.endpoint_obj.to_dict()
        # override the default output from pydantic by calling `to_dict()` of user
        if self.user:
            _dict['user'] = self.user.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ConnectionToken from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pk": obj.get("pk"),
            "provider": obj.get("provider"),
            "provider_obj": RACProvider.from_dict(obj["provider_obj"]) if obj.get("provider_obj") is not None else None,
            "endpoint": obj.get("endpoint"),
            "endpoint_obj": Endpoint.from_dict(obj["endpoint_obj"]) if obj.get("endpoint_obj") is not None else None,
            "user": GroupMember.from_dict(obj["user"]) if obj.get("user") is not None else None
        })
        return _obj


