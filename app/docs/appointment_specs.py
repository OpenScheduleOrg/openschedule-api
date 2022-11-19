from .responses import created_201, updated_200, \
    validation_response_422, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

appointment_minimal = {
    "type": "object",
    "properties": {
        "complaint": {
            "type": "string",
            "example": ""
        },
        "prescription": {
            "type": "string",
            "example": ""
        },
        "scheduled_day": {
            "type": "string",
            "format": "date",
            "example": "2022-12-20"
        },
        "start_time": {
            "type": "integer",
            "example": 420
        },
        "end_time": {
            "type": "integer",
            "example": 440
        },
        "patient_id": {
            "type": "integer",
            "example": 3
        },
        "acting_id": {
            "type": "integer",
            "example": 1
        }
    }
}

appointment_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
        },
        "patient_name": {
            "type": "string",
            "example": "Foo Bar Jr"
        },
        "clinic_id": {
            "type": "integer",
            "example": 3
        },
        "clinic_name": {
            "type": "string",
            "example": "Institution health"
        },
        "professional_id": {
            "type": "integer",
            "example": 9
        },
        "professional_name": {
            "type": "string",
            "example": "Foo Bar"
        },
        "specialty_id": {
            "type": "integer",
            "example": 9
        },
        "specialty_description": {
            "type": "string",
            "example": "Foolist"
        },
        **appointment_minimal["properties"], "created_at": {
            "type": "string",
            "format": "date-time",
            "example": "2022-09-22 14:38:23"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time",
            "example": "2022-09-22 18:38:23"
        }
    }
}

tags = {
    "tags": [{
        "name": "appointments",
    }]
}

post_appointment = {
    **tags, "summary": "Create appointment",
    "description": "Create a new appointment",
    "opeartionId": "post_appointment",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": appointment_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Appointment"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_appointments = {
    **tags, "summary":
    "Load appointments",
    "description":
    "Filter and load appointments with pagination",
    "opeartionId":
    "get_appointments",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "page",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
            "default": 1
        }
    }, {
        "name": "limit",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
            "default": 20
        }
    }, {
        "name": "acting_id",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "patient_id",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "clinic_id",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "professional_id",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "specialty_id",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": list_response_200("Appointment"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_appointment_by_id = {
    **tags, "summary":
    "Load a appointment",
    "description":
    "load appointment by id",
    "opeartionId":
    "get_appointment_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "appointment_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Appointment"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_appointment = {
    **tags, "summary":
    "Update appointment",
    "description":
    "update a appointment using id",
    "opeartionId":
    "put_appointment",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "appointment_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": appointment_minimal
            }
        }
    },
    "responses": {
        "200": updated_200("Appointment"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_appointment = {
    **tags, "summary":
    "Delete appointment",
    "description":
    "update a appointment using id",
    "opeartionId":
    "delete_appointment",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "appointment_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "204": not_content_success_204,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}
