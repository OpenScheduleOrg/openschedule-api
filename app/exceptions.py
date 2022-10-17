from flask import jsonify, request, current_app

from .constants import ResponseMessages


class APIException(Exception):

    def __init__(self, message, status_code=400, detail=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.detail = detail

    def to_dict(self):
        """
        Result dict a bad request with erro
        """
        rv = {"message": self.message}
        if self.detail is not None:
            rv["detail"] = self.detail

        return rv


class ValidationException(Exception):

    def __init__(self, errors: dict[str, str]):
        super().__init__()
        self.errors = errors


def resource_not_found(_):
    """
    Default return not found endpoint
    """
    return jsonify({
        "message": "Resource not found.",
        "path": request.full_path
    }), 404


def internal_server_error(e):
    """
    Handle with server's errors
    """
    current_app.logger.error(e)
    return jsonify({"message": ResponseMessages.UNEXPECTED_ERROR}), 500


def api_exception_handler(e):
    """
    Handle api exception
    """
    e_json = e.to_dict()
    return jsonify(e_json), e.status_code


def validation_exception_handler(e: ValidationException):
    """
    Handle api exception
    """
    return jsonify(e.errors), 400
