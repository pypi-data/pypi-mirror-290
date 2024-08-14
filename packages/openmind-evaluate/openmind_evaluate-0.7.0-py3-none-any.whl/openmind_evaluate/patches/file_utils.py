# Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
from functools import wraps
from evaluate.utils import logging

logger = logging.get_logger(__name__)


def request_with_retry_wrapper(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        resp = fn(*args, **kwargs)
        if resp.status_code == 404:
            raise FileNotFoundError
        return resp

    return wrapper


def get_authentication_headers_for_url_wrapper(fn):
    @wraps(fn)
    def wrapper(url, use_auth_token=None):
        return fn(url=url, use_auth_token=None)

    return wrapper
