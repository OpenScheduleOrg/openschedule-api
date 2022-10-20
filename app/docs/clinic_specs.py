from .responses import created_201, updated_200, \
    validation_response_400, unauthenticated_user_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

clinic_minimal = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "example": "Institution health"
        },
        "type": {
            "type": "integer",
            "description": "enum with type of clinic",
            "example": 2
        },
        "cnpj": {
            "type": "string",
            "example": "68.927.406/0001-58"
        },
        "phone": {
            "type": "string",
            "example": "(61) 3657-4513"
        },
        "address": {
            "type": "string",
            "example": "Centro, 888, 632232-000, Cidade"
        },
        "longitude": {
            "type": "string",
            "example": "-5.037320"
        },
        "latitude": {
            "type": "string",
            "example": "-42.450742"
        }
    }
}

clinic_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
        },
        **clinic_minimal["properties"], "created_at": {
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
        "name": "clinics",
    }]
}

post_clinic = {
    **tags, "summary": "Create clinic",
    "description": "Any description about post clinic",
    "opeartionId": "post_clinic",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": clinic_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Clinic"),
        "400": validation_response_400,
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}

get_clinics = {
    **tags, "summary":
    "Load clinics",
    "description":
    "Filter and load clinics with pagination",
    "opeartionId":
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
        "name": "type",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "cnpj",
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
        "200": list_response_200("Clinic"),
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}

get_clinic_by_id = {
    **tags, "summary":
    "Load a clinic",
    "description":
    "load clinic by id",
    "opeartionId":
    "get_clinic_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Clinic"),
        "404": entity_not_found_404,
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}

get_clinic_by_cnpj = {
    **tags, "summary":
    "Load a clinic using cnpj",
    "description":
    "load clinic by cnpj",
    "opeartionId":
    "get_clinic_by_cnpj",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_cnpj",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Clinic"),
        "404": entity_not_found_404,
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}

get_clinic_by_phone = {
    **tags, "summary":
    "Load a clinic phone",
    "description":
    "load clinic by phone",
    "opeartionId":
    "get_clinic_by_phone",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_phone",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Clinic"),
        "404": entity_not_found_404,
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}

update_clinic = {
    **tags, "summary":
    "Update clinic",
    "description":
    "update a clinic using id",
    "opeartionId":
    "put_clinic",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_id",
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
                "schema": clinic_minimal
            }
        }
    },
    "responses": {
        "200": updated_200("Clinic"),
        "400": validation_response_400,
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}

delete_clinic = {
    **tags, "summary":
    "Delete clinic",
    "description":
    "delete clinic using id",
    "opeartionId":
    "delete_clinic",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "204": not_content_success_204,
        "401": unauthenticated_user_401,
        "403": not_authorized_403,
    }
}
