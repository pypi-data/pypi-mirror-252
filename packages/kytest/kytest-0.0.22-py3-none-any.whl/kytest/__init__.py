from .case import (
    ApiCase,
    AdrCase,
    IosCase,
    WebCase
)
from .page import Page
from .running.runner import main
from .utils.config import config
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .utils.exceptions import KError


__version__ = "0.0.22"
__description__ = "API/安卓/IOS/WEB平台自动化测试框架"
