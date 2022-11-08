from .responses import created_201, updated_200, \
    validation_response_422, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

professional_acting = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number",
            "example": "69"
        },
        "clinic_id": {
            "type": "number",
            "example": "80"
        },
        "clinic_name": {
            "type": "string",
            "example": "Clinic name"
        },
        "specialty_id": {
            "type": "number",
            "example": "90"
        },
        "specialty_description": {
            "type": "string",
            "example": "Clinic name"
        },
    }
}

professional_minimal = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "example": "Professional Foo Bar"
        },
        "phone": {
            "type": "string",
            "example": "(99) 99999-9999"
        },
        "reg_number": {
            "type": "string",
            "example": "9999"
        },
        "username": {
            "type": "string",
            "example": "profoobar23"
        },
        "email": {
            "type": "string",
            "example": "foo@bar.prof",
        },
        "password": {
            "type": "string",
            "example": "supersecret"
        }
    }
}

professional_update = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "example": "Professional Foo Bar"
        },
        "phone": {
            "type": "string",
            "example": "(99) 99999-9999"
        },
        "reg_number": {
            "type": "string",
            "example": "9999"
        },
        "username": {
            "type": "string",
            "example": "profoobar23"
        },
        "email": {
            "type": "string",
            "example": "foo@bar.prof",
        }
    }
}

professional_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
        },
        **professional_minimal["properties"], "created_at": {
            "type": "string",
            "format": "date-time",
            "example": "2022-09-22 14:38:23"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time",
            "example": "2022-09-22 18:38:23"
        },
        "actuations": {
            "type": "array",
            "items": {
                "$ref": "#/components/schemas/ProfessionalActing"
            }
        }
    }
}

tags = {
    "tags": [{
        "name": "professionals",
    }]
}

post_professional = {
    **tags, "summary": "Create professional",
    "description": "Create a new professional",
    "opeartionId": "post_professional",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": professional_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Professional"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_professionals = {
    **tags, "summary":
    "Load professionals",
    "description":
    "Filter and load professionals with pagination",
    "opeartionId":
    "get_professionals",
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
        "name": "phone",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }, {
        "name": "reg_number",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }, {
        "name": "username",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }, {
        "name": "email",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": list_response_200("Professional"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_professional_by_id = {
    **tags, "summary":
    "Load a professional",
    "description":
    "load professional by id",
    "opeartionId":
    "get_professional_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "professional_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Professional"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_professional_by_phone = {
    **tags, "summary":
    "Load a professional using phone",
    "description":
    "load professional by phone",
    "opeartionId":
    "get_professional_by_phone",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "professional_phone",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Professional"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_professional_by_username = {
    **tags, "summary":
    "Load a professional using username",
    "description":
    "load professional by username",
    "opeartionId":
    "get_professional_by_username",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "professional_username",
        "in": "path",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Professional"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_professional_by_email = {
    **tags, "summary":
    "Load a professional email",
    "description":
    "load professional by email",
    "opeartionId":
    "get_professional_by_email",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "professional_email",
        "in": "path",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("Professional"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_professional = {
    **tags, "summary":
    "Update professional",
    "description":
    "update a professional using id",
    "opeartionId":
    "put_professional",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "professional_id",
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
                "schema": professional_update
            }
        }
    },
    "responses": {
        "200": updated_200("Professional"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_professional = {
    **tags, "summary":
    "Delete professional",
    "description":
    "update a professional using id",
    "opeartionId":
    "delete_professional",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "professional_id",
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
