__all__ = [
    'parse_html',
    'driver',
    'fetch_html',
    'web_configs',
    'WebConfig'
]

from .parse_html import *
from .fetch_html import *
from .driver import *
from .web_config import *

web_configs = WebConfig.configs