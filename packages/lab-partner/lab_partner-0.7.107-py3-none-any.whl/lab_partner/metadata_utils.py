import sys
from importlib import metadata


def lab_version():
    return metadata.version('lab-partner')


def is_linux() -> bool:
    """
    Check current platform is Linux
    :return: True on Linux
    """
    return sys.platform in ('linux',)
