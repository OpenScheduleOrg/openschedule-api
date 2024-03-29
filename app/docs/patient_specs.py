from .responses import created_201, updated_200, \
    validation_response_422, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

patient_minimal = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "example": "Foo Bar"
        },
        "cpf": {
            "type": "string",
            "example": "325.553.790-88"
        },
        "registration": {
            "type": "string",
            "example": "20201P2ADS0188"
        },
        "phone": {
            "type": "string",
            "example": "(69) 93657-4513"
        },
        "address": {
            "type": "string",
            "example": "Centro, 888, 632232-000, Cidade"
        },
        "birthdate": {
            "type": "string",
            "format": "date",
            "example": "2000-01-01"
        },
    }
}

patient_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
        },
        **patient_minimal["properties"], "created_at": {
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
        "name": "patients",
    }]
}

post_patient = {
    **tags, "summary": "Create patient",
    "description": "Create a new patient",
    "operationId": "post_patient",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": patient_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Patient"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_patients = {
    **tags, "summary":
    "Load patients",
    "description":
    "Filter and load patients with pagination",
    "operationId":
    "get_clinics",
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
        "name": "name",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }, {
        "name": "cpf",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }, {
        "name": "registration",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }, {
        "name": "phone",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": list_response_200("Patient"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_patient_by_id = {
    **tags, "summary":
    "Load a patient",
    "description":
    "load patient by id",
    "operationId":
    "get_patient_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "patient_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Patient"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_patient_by_cpf = {
    **tags, "summary":
    "Load a patient using cpf",
    "description":
    "load patient by cpf",
    "operationId":
    "get_patient_by_cpf",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "patient_cpf",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Patient"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_patient_by_registration = {
    **tags, "summary":
    "Load a patient using registration",
    "description":
    "load patient by registration",
    "operationId":
    "get_patient_by_registration",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "patient_registration",
        "in": "path",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Patient"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_patient_by_phone = {
    **tags, "summary":
    "Load a patient phone",
    "description":
    "load patient by phone",
    "operationId":
    "get_patient_by_phone",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "patient_phone",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Patient"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_patient = {
    **tags, "summary":
    "Update patient",
    "description":
    "update a patient using id",
    "operationId":
    "put_patient",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "patient_id",
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
                "schema": patient_minimal
            }
        }
    },
    "responses": {
        "200": updated_200("Patient"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_patient = {
    **tags, "summary":
    "Delete patient",
    "description":
    "update a patient using id",
    "operationId":
    "delete_patient",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "patient_id",
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
