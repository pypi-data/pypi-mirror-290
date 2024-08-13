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


class LicenseSummaryStatusEnum(str, Enum):
    """
    LicenseSummaryStatusEnum
    """

    """
    allowed enum values
    """
    UNLICENSED = 'unlicensed'
    VALID = 'valid'
    EXPIRED = 'expired'
    EXPIRY_SOON = 'expiry_soon'
    LIMIT_EXCEEDED_ADMIN = 'limit_exceeded_admin'
    LIMIT_EXCEEDED_USER = 'limit_exceeded_user'
    READ_ONLY = 'read_only'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of LicenseSummaryStatusEnum from a JSON string"""
        return cls(json.loads(json_str))


