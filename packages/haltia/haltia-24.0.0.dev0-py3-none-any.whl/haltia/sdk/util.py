# This is free and unencumbered software released into the public domain.

"""The Haltia.AI Software Development Kit (SDK) for Python."""

from . import abi

def licensee() -> str:
    """
    Returns the name and email of who the loaded SDK build is licensed to.

    The licensee string format is "J. Random Hacker <jhacker@example.com>".
    """
    return abi.haiGetLicenseeString().decode('utf-8', 'replace')

def version() -> str:
    """
    Returns the full version string for the loaded SDK build.

    The version string format is "24.0.0-dev.123 (2024-01-31)".

    Note that this version is likely to be different from the Python SDK
    library version. The two are compatible so long as the two initial
    major components of the version string are equivalent for both.
    """
    return abi.haiGetVersionString().decode('utf-8', 'replace')
