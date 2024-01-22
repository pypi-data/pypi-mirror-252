from . import _version
import logging

__version__ = _version.get_versions()['version']

from .endpointsdb import endpointsdb
from .ouidb import ouidb
from .parser import parser

logger = logging.getLogger(__name__)