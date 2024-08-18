# -*- coding: utf-8 -*-

import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
