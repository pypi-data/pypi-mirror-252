from __future__ import annotations

import re
from typing import Annotated, Optional

from annotated_types import Ge, Le
from ormspace.keys import TableKey
from ormspace.metainfo import MetaInfo
from pydantic import AfterValidator, BeforeValidator, Field


def string_to_list(string: str|list) -> list:
    if not string:
        return list()
    if isinstance(string, str):
        return [i.strip() for i in re.split(r'[+\n;]', string) if i]
    return string

def none_if_empty_string(string: str|None) -> str|None:
    if string == '':
        return None
    return string

def body_measure_range(value: float | int | None) -> str|None:
    if value is not None:
        if value < 0:
            raise ValueError('Value must be greater than 0')
        elif value > 300:
            raise ValueError('Value must be lesser than 300')
    return value


StringList = Annotated[list[str], BeforeValidator(string_to_list), Field(default_factory=list)]
ProfileKey = Annotated[TableKey, MetaInfo(tables=['Patient', 'Doctor', 'Employee'], item_name='profile'), Field('Doctor.admin')]
StaffKey = Annotated[TableKey, MetaInfo(tables=['Doctor', 'Employee'], item_name='staff'), Field('Doctor.admin')]
OptionalFloat = Annotated[Optional[float], BeforeValidator(none_if_empty_string), Field(None)]
OptionalInteger = Annotated[Optional[int], BeforeValidator(none_if_empty_string), Field(None)]
BodyMeasureFloat = Annotated[OptionalFloat, AfterValidator(body_measure_range)]
BodyMeasureInteger = Annotated[OptionalInteger, AfterValidator(body_measure_range)]