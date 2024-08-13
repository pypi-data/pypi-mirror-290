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
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from authentik_client.models.apple_login_challenge import AppleLoginChallenge
from authentik_client.models.plex_authentication_challenge import PlexAuthenticationChallenge
from authentik_client.models.redirect_challenge import RedirectChallenge
from pydantic import StrictStr, Field
from typing import Union, List, Optional, Dict
from typing_extensions import Literal, Self

LOGINCHALLENGETYPES_ONE_OF_SCHEMAS = ["AppleLoginChallenge", "PlexAuthenticationChallenge", "RedirectChallenge"]

class LoginChallengeTypes(BaseModel):
    """
    LoginChallengeTypes
    """
    # data type: RedirectChallenge
    oneof_schema_1_validator: Optional[RedirectChallenge] = None
    # data type: PlexAuthenticationChallenge
    oneof_schema_2_validator: Optional[PlexAuthenticationChallenge] = None
    # data type: AppleLoginChallenge
    oneof_schema_3_validator: Optional[AppleLoginChallenge] = None
    actual_instance: Optional[Union[AppleLoginChallenge, PlexAuthenticationChallenge, RedirectChallenge]] = None
    one_of_schemas: List[str] = Field(default=Literal["AppleLoginChallenge", "PlexAuthenticationChallenge", "RedirectChallenge"])

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = LoginChallengeTypes.model_construct()
        error_messages = []
        match = 0
        # validate data type: RedirectChallenge
        if not isinstance(v, RedirectChallenge):
            error_messages.append(f"Error! Input type `{type(v)}` is not `RedirectChallenge`")
        else:
            match += 1
        # validate data type: PlexAuthenticationChallenge
        if not isinstance(v, PlexAuthenticationChallenge):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PlexAuthenticationChallenge`")
        else:
            match += 1
        # validate data type: AppleLoginChallenge
        if not isinstance(v, AppleLoginChallenge):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AppleLoginChallenge`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in LoginChallengeTypes with oneOf schemas: AppleLoginChallenge, PlexAuthenticationChallenge, RedirectChallenge. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in LoginChallengeTypes with oneOf schemas: AppleLoginChallenge, PlexAuthenticationChallenge, RedirectChallenge. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into RedirectChallenge
        try:
            instance.actual_instance = RedirectChallenge.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into PlexAuthenticationChallenge
        try:
            instance.actual_instance = PlexAuthenticationChallenge.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AppleLoginChallenge
        try:
            instance.actual_instance = AppleLoginChallenge.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into LoginChallengeTypes with oneOf schemas: AppleLoginChallenge, PlexAuthenticationChallenge, RedirectChallenge. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into LoginChallengeTypes with oneOf schemas: AppleLoginChallenge, PlexAuthenticationChallenge, RedirectChallenge. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], AppleLoginChallenge, PlexAuthenticationChallenge, RedirectChallenge]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


