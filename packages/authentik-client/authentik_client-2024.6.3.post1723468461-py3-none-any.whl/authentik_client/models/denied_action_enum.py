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
from enum import Enum
from typing_extensions import Self


class DeniedActionEnum(str, Enum):
    """
    DeniedActionEnum
    """

    """
    allowed enum values
    """
    MESSAGE_CONTINUE = 'message_continue'
    MESSAGE = 'message'
    CONTINUE = 'continue'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DeniedActionEnum from a JSON string"""
        return cls(json.loads(json_str))


