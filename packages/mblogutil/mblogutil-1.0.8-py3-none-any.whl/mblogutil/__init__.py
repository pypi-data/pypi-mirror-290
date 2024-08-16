from importlib import resources
from os import path

from .logger import get

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "1.0.8"

_cfg = tomllib.loads(resources.read_text("mblogutil", "config.toml"))
ROTATING = bool(_cfg['filehandler']['rotating'])
MAXBYTES = int(_cfg['filehandler']['maxbytes'])
BACKUPCOUNT = int(_cfg['filehandler']['backupcount'])