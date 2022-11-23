from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dataraster")
except PackageNotFoundError:
    pass

from .app import app as dataraster
