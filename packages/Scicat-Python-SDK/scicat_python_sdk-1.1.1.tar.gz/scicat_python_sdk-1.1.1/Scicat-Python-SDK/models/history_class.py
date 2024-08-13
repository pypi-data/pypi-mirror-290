# coding: utf-8

"""
    SciCat backend API

    This is the API for the SciCat Backend

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class HistoryClass(BaseModel):
    """
    HistoryClass
    """ # noqa: E501
    id: StrictStr = Field(description="Persistent Identifier for datasets derived from UUIDv4 and prepended automatically by site specific PID prefix like 20.500.12345/")
    updated_at: datetime = Field(description="Time when the update was performed. This field is managed by mongoose with through the timestamp settings. The field should be a string containing a date in ISO 8601 format (2024-02-27T12:26:57.313Z)", alias="updatedAt")
    updated_by: StrictStr = Field(description="Username of the user that performed the update.", alias="updatedBy")
    __properties: ClassVar[List[str]] = ["id", "updatedAt", "updatedBy"]

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
        """Create an instance of HistoryClass from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of HistoryClass from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id") if obj.get("id") is not None else '3c204cfa-3e7b-44c5-8c45-32cf9c1953d3',
            "updatedAt": obj.get("updatedAt"),
            "updatedBy": obj.get("updatedBy")
        })
        return _obj


