###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, Union, Literal

from . import types
from .types import Checked, Check

###############################################################################
#
#  These types are used for streaming, for when an instance of a type
#  is still being built up and any of its fields is not yet fully available.
#
###############################################################################


class Attribute(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    data_type: Optional[types.DataType] = None

class Entity(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    attributes: List["Attribute"]

class KGOutput(BaseModel):
    entities: List["Entity"]
