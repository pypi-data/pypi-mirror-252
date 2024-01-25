import logging
import os

from logtail import LogtailHandler

LOGGER_IS_NOT_INITIALIZED = True


def collect_logger():
    result_logger = logging.getLogger(__name__)
    global LOGGER_IS_NOT_INITIALIZED
    if LOGGER_IS_NOT_INITIALIZED:
        LOGGER_IS_NOT_INITIALIZED = False
        log_token = os.getenv("SOURCE_TOKEN")
        if log_token is None:
            result_logger.info("initialized local logger")
        else:
            handler = LogtailHandler(source_token=log_token)
            partially_constructed_logger = logging.getLogger(__name__)
            partially_constructed_logger.setLevel(logging.INFO)
            log_format = logging.Formatter("%(message)s")
            handler.setFormatter(log_format)
            partially_constructed_logger.handlers = []
            partially_constructed_logger.addHandler(handler)
            result_logger.info("initialized betterstack logger")
    return result_logger


logger = collect_logger()


class Response:
    def __init__(self, status_code, success, content, error):
        self.status_code = status_code
        self.success = success
        self.content = content
        self.error = error

    def __eq__(self, other):
        return self.status_code == other.status_code \
            and self.success == other.success \
            and self.content == other.content \
            and self.error == other.error

    def __repr__(self):
        return f"Response(<{self.status_code}> | success: {self.success} | content: {self.content} | error: " \
               f"{self.error})"

    def flaskify(self):
        return {
            "success": self.success,
            "error": self.error,
            "content": self.content
        }, self.status_code


def create_response(content):
    response = Response(
        status_code=200,
        success=True,
        content=content,
        error=""
    )
    logger.info("generating success response", extra={"content": response.flaskify()[0], "status_code": 200})
    return response


def create_upstream_failure_response(error):
    return create_error_response(515, error)


def create_error_response(status_code, error):
    response = Response(
        status_code=status_code,
        success=False,
        content={},
        error=error
    )
    logger.info("generating failure response", extra={"content": response.flaskify()[0], "status_code": status_code})
    return response


class ExtractionFailure(Exception):
    pass
