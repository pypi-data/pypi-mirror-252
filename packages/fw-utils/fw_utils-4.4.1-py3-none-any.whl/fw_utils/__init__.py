"""Flywheel utilities and common helpers."""
from importlib.metadata import version
from json import JSONEncoder

__version__ = version(__name__)
__all__ = [
    "ZoneInfo",
    "format_datetime",
    "get_datetime",
    "get_tzinfo",
    "AttrDict",
    "attrify",
    "flatten_dotdict",
    "get_field",
    "inflate_dotdict",
    "AnyFile",
    "AnyPath",
    "BinFile",
    "TempDir",
    "TempFile",
    "fileglob",
    "open_any",
    "BaseFilter",
    "ExpressionFilter",
    "Filters",
    "IncludeExcludeFilter",
    "NumberFilter",
    "SetFilter",
    "SizeFilter",
    "StringFilter",
    "TimeFilter",
    "Template",
    "Timer",
    "format_query_string",
    "format_template",
    "format_url",
    "hrsize",
    "hrtime",
    "pluralize",
    "quantify",
    "report_progress",
    "Pattern",
    "parse_field_name",
    "parse_hrsize",
    "parse_hrtime",
    "parse_pattern",
    "parse_url",
    "Cached",
    "TempEnv",
    "assert_like",
]

from .datetime import ZoneInfo, format_datetime, get_datetime, get_tzinfo
from .dicts import AttrDict, attrify, flatten_dotdict, get_field, inflate_dotdict
from .files import AnyFile, AnyPath, BinFile, TempDir, TempFile, fileglob, open_any
from .filters import (
    BaseFilter,
    ExpressionFilter,
    Filters,
    IncludeExcludeFilter,
    NumberFilter,
    SetFilter,
    SizeFilter,
    StringFilter,
    TimeFilter,
)
from .formatters import (
    Template,
    Timer,
    format_query_string,
    format_template,
    format_url,
    hrsize,
    hrtime,
    pluralize,
    quantify,
    report_progress,
)
from .json import json_encoder
from .parsers import (
    Pattern,
    parse_field_name,
    parse_hrsize,
    parse_hrtime,
    parse_pattern,
    parse_url,
)
from .state import Cached, TempEnv
from .testing import assert_like

# patch / extend the built-in python json encoder
setattr(JSONEncoder, "orig_default", JSONEncoder.default)
setattr(JSONEncoder, "default", json_encoder)
