from .clinic_specs import clinic_model
from .patient_specs import patient_model

swagger_template = {
    "openapi": "3.0.2",
    "info": {
        "title": "Consuchat API",
        "description": "",
        "contact": {
            "email": "azurique10111@gmail.com",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "termsOfService": "http://consuchat.com/terms",
        "version": "0.5.0"
    },
    "servers": [{
        "url": "http://localhost:5000/api"
    }],
    "basePath": "/api",
    "components": {
        "schemas": {
            "Clinic": clinic_model,
            "Patient": patient_model,
            "ValidationResponse": {
                "type": "object",
                "properties": {
                    "[fieldName]": {
                        "type": "string",
                        "description": "validation message",
                        "example": "Field birthdate is not a date"
                    }
                }
            },
            "SimpleMessageResponse": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example":
                        "message describing the reason for the response"
                    }
                }
            },
        }
    }
}

swagger_config = {
    "headers": [],
    "openapi":
    "3.0.2",
    "specs": [{
        "endpoint": 'apispec_v1',
        "route": '/apispec_v1.json',
        "rule_filter": lambda rule: True,  # all in
        "model_filter": lambda tag: True,  # all in
    }],
    "static_url_path":
    "/flasgger_static",
    "swagger_ui":
    True,
    "specs_route":
    "/apidocs/"
}