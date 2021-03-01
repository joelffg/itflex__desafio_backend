import re
from functools import wraps
from http import HTTPStatus
from traceback import print_exc
from typing import Tuple, Union

from flask import Response, request as http_req

from . import json
from .response import ErrorTypes, FieldError, Status

__all__ = ["API", "dump_errors", "http_status"]

REFRESH_TOKEN_EXP = 30 * 24 * 60 * 60

TOKEN_REGEX = re.compile(r"^Bearer +(?P<token>.*)$")

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT = "text/plain"

HTTP_STATUS_MAP = {
    Status.ok: HTTPStatus.OK,
    Status.not_found: HTTPStatus.NOT_FOUND,
    Status.invalid: HTTPStatus.BAD_REQUEST,
    Status.duplicated: HTTPStatus.CONFLICT,
    Status.conflict: HTTPStatus.CONFLICT,
    Status.unauthenticated: HTTPStatus.UNAUTHORIZED,
    Status.forbidden: HTTPStatus.FORBIDDEN,
    Status.server_error: HTTPStatus.INTERNAL_SERVER_ERROR,
    Status.unprocessable_entry: HTTPStatus.UNPROCESSABLE_ENTITY,
}
HTTP_ERROR_MAP = {
    ErrorTypes.invalid: "invalid",
    ErrorTypes.duplicated: "duplicated",
    ErrorTypes.required: "required",
    ErrorTypes.not_found: "not_found",
    ErrorTypes.rule: "rule",
}

StrLike = Union[str, bytes]
HttpBody = Union[dict, StrLike]
HttpResp = Union[HttpBody, Tuple[HttpBody, Status], Response]


class API:
    json_resp = True

    def __init__(self):
        self._methods = []

        for method in ["get", "post", "put", "patch", "delete"]:
            if hasattr(self, method):
                self._methods.append(method.upper())

    @property
    def methods(self):
        return self._methods

    def _handle_return(self, ret: HttpResp, status: Status = None):
        if status is None:
            status = HTTPStatus.OK

        if isinstance(status, Status):
            status = http_status(status)

        if isinstance(ret, dict):
            return Response(
                json.dumps(ret),
                status=status,
                headers={"Content-Type": CONTENT_TYPE_JSON},
            )
        elif isinstance(ret, str):
            return Response(
                ret, status=status, headers={"Content-Type": CONTENT_TYPE_TEXT}
            )

        if isinstance(ret, tuple):
            ret, status = ret
            return self._handle_return(ret, status)

        return ret

    def __call__(self, *args, **kwargs) -> Response:
        if http_req.method not in self._methods:
            return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

        try:
            if http_req.method == "GET":
                return self._handle_return(self.get(*args, **kwargs))
            if http_req.method == "POST":
                return self._handle_return(self.post(*args, **kwargs))
            if http_req.method == "PUT":
                return self._handle_return(self.put(*args, **kwargs))
            if http_req.method == "PATCH":
                return self._handle_return(self.patch(*args, **kwargs))
            if http_req.method == "DELETE":
                return self._handle_return(self.delete(*args, **kwargs))
        except Exception as e:
            print_exc()
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


def headers(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        kwargs["headers"] = dict(http_req.headers)
        return func(self, *args, **kwargs)

    return wrapper


def json_body(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not http_req.is_json:
            return Response(
                "This API only supports requests encoded as JSON",
                status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )

        try:
            body = json.loads(http_req.data)
        except ValueError:
            return Response(
                "This API only supports requests encoded as JSON",
                status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )

        if not isinstance(body, dict):
            return Response(
                "This API only supports requests encoded as JSON",
                status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )

        return func(self, body, *args, **kwargs)

    return wrapper


def form_data_body(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        files = http_req.files
        body = {}

        for key, value in http_req.form.items():
            body[key] = value

        return func(self, body, files, *args, **kwargs)

    return wrapper


def dump_errors(errors):
    if not errors:
        return ""

    errors_data = []
    for error in errors:
        if not isinstance(error, FieldError):
            data = {
                "field": error.field,
                "type": error.json().get("type"),
                "msg": error.message,
            }
            if error.value:
                data["params"] = error.value
        else:
            data = {
                "field": error.field,
                "type": HTTP_ERROR_MAP[error.type],
                "msg": "",
            }
            if error.msg:
                data["msg"] = error.msg
            if error.params:
                data["params"] = error.params

        errors_data.append(data)

    return {"errors": errors_data}


def http_status(status):
    return HTTP_STATUS_MAP.get(status, HTTPStatus.INTERNAL_SERVER_ERROR)

