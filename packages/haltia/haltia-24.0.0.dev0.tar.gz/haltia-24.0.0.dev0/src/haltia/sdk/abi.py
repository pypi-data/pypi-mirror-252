# This is free and unencumbered software released into the public domain.

"""The Haltia.AI Software Development Kit (SDK) for Python."""

from warnings import warn
from .lib import *

lib = load_library()

# const char* haiGetLicenseeString()
try:
    haiGetLicenseeString = lib.haiGetLicenseeString
    haiGetLicenseeString.restype = c_char_p
    haiGetLicenseeString.argtypes = ()
except AttributeError as err:
    warn(err, ImportWarning)

# const char* haiGetVersionString()
try:
    haiGetVersionString = lib.haiGetVersionString
    haiGetVersionString.restype = c_char_p
    haiGetVersionString.argtypes = ()
except AttributeError as err:
    warn(err, ImportWarning)

__all__ = [
    'haiGetLicenseeString',
    'haiGetVersionString',
]
