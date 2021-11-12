from flask import jsonify, request

def resource_not_found(error):
    return jsonify({"status": "fail", "message": "Resource not found" , "path": request.full_path})


class APIExceptionHandler(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, status="fail", detail=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.detail = detail
        self.status = status

    def to_dict(self):
        rv = dict()
        rv["status"] = self.status
        rv["message"] = self.message
        rv["data"] = {}
        if self.detail is not None:
            rv["data"]["detail"] = self.detail

        return rv

def api_exception_handler(e):
    e_json = e.to_dict()
    e_json["data"]["payload"] = request.get_json()

    return jsonify(e_json), e.status_code

