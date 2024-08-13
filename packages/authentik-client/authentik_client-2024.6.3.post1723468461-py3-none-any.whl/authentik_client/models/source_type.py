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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class SourceType(BaseModel):
    """
    Serializer for SourceType
    """ # noqa: E501
    name: StrictStr
    verbose_name: StrictStr
    urls_customizable: StrictBool
    request_token_url: Optional[StrictStr]
    authorization_url: Optional[StrictStr]
    access_token_url: Optional[StrictStr]
    profile_url: Optional[StrictStr]
    oidc_well_known_url: Optional[StrictStr]
    oidc_jwks_url: Optional[StrictStr]
    __properties: ClassVar[List[str]] = ["name", "verbose_name", "urls_customizable", "request_token_url", "authorization_url", "access_token_url", "profile_url", "oidc_well_known_url", "oidc_jwks_url"]

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
        """Create an instance of SourceType from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "request_token_url",
            "authorization_url",
            "access_token_url",
            "profile_url",
            "oidc_well_known_url",
            "oidc_jwks_url",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if request_token_url (nullable) is None
        # and model_fields_set contains the field
        if self.request_token_url is None and "request_token_url" in self.model_fields_set:
            _dict['request_token_url'] = None

        # set to None if authorization_url (nullable) is None
        # and model_fields_set contains the field
        if self.authorization_url is None and "authorization_url" in self.model_fields_set:
            _dict['authorization_url'] = None

        # set to None if access_token_url (nullable) is None
        # and model_fields_set contains the field
        if self.access_token_url is None and "access_token_url" in self.model_fields_set:
            _dict['access_token_url'] = None

        # set to None if profile_url (nullable) is None
        # and model_fields_set contains the field
        if self.profile_url is None and "profile_url" in self.model_fields_set:
            _dict['profile_url'] = None

        # set to None if oidc_well_known_url (nullable) is None
        # and model_fields_set contains the field
        if self.oidc_well_known_url is None and "oidc_well_known_url" in self.model_fields_set:
            _dict['oidc_well_known_url'] = None

        # set to None if oidc_jwks_url (nullable) is None
        # and model_fields_set contains the field
        if self.oidc_jwks_url is None and "oidc_jwks_url" in self.model_fields_set:
            _dict['oidc_jwks_url'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SourceType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "verbose_name": obj.get("verbose_name"),
            "urls_customizable": obj.get("urls_customizable"),
            "request_token_url": obj.get("request_token_url"),
            "authorization_url": obj.get("authorization_url"),
            "access_token_url": obj.get("access_token_url"),
            "profile_url": obj.get("profile_url"),
            "oidc_well_known_url": obj.get("oidc_well_known_url"),
            "oidc_jwks_url": obj.get("oidc_jwks_url")
        })
        return _obj


