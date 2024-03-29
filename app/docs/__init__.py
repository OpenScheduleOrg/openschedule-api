from .clinic_specs import clinic_model
from .patient_specs import patient_model
from .user_specs import user_model
from .professional_specs import professional_model, professional_acting
from .specialty_specs import specialty_model
from .acting_specs import acting_model
from .schedule_specs import schedule_model
from .appointment_specs import appointment_model

swagger_template = {
    "openapi": "3.0.2",
    "info": {
        "title": "Open Schedule API",
        "description": "",
        "contact": {
            "email": "azurique10111@gmail.com",
        },
        "license": {
            "name": "BSD 3-Clause",
            "url": "https://opensource.org/licenses/BSD-3-Clause"
        },
        "termsOfService": "http://openshedule.org/terms",
        "version": "0.5.0"
    },
    "servers": [],
    "basePath": "/",
    "components": {
        "schemas": {
            "Clinic": clinic_model,
            "Patient": patient_model,
            "User": user_model,
            "Professional": professional_model,
            "ProfessionalActing": professional_acting,
            "Specialty": specialty_model,
            "Acting": acting_model,
            "Schedule": schedule_model,
            "Appointment": appointment_model,
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
        },
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
            "BearerAuthSession": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
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
