# This is free and unencumbered software released into the public domain.

"""The Haltia.AI Software Development Kit (SDK) for Python."""

import os
import platform

from ctypes import *

MACOS_APP_PATH = 'Applications/Haltia.AI.app'
MACOS_APP_SUBPATH = 'Contents/Frameworks/HaltiaAI.framework/HaltiaAI'
MACOS_SDK_DYLIB = 'libHaltiaAI.dylib'

def load_library() -> CDLL:
    for path in paths():
        try:
            return cdll.LoadLibrary(path)
        except OSError as err:
            #print(err)
            pass
    raise ModuleNotFoundError("Unable to find the Haltia.AI SDK binaries")

def paths() -> list[str]:
    result = []
    sys = platform.system()

    if sys == 'Darwin':  # macOS
        if (path := os.getenv('HALTIA_SDK')) is not None:
            result.append(path)
        if (path := os.getenv('HALTIA_APP')) is not None:
            result.append(os.path.join(path, MACOS_APP_SUBPATH))
        if (path := os.getenv('HOME')) is not None:
            result.append(os.path.join(path, MACOS_APP_PATH, MACOS_APP_SUBPATH))
        result.append(os.path.join('/', MACOS_APP_PATH, MACOS_APP_SUBPATH))
        result.append(MACOS_SDK_DYLIB)

    elif sys == 'Linux':
        result.append('libHaltiaAI.so')

    elif sys == 'Windows':
        result.append('HaltiaAI.dll')

    return list(dict.fromkeys(result))  # remove duplicates
