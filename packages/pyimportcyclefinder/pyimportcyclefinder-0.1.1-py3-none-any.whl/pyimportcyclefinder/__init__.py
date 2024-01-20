"""

"""


def _auto_version():
    try:
        from ._version import __version__
        return __version__
    except ModuleNotFoundError:
        pass
    try:
        from .auto_version import generate_version_string_for_scenario
        return generate_version_string_for_scenario()
    except RuntimeError:
        return 'unknown [could not determine automatically, do you not have git?]'


__version__ = _auto_version()
__all__ = ["__version__"]
