from .responses import created_201, updated_200, \
    validation_response_400, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

specialty_minimal = {
    "type": "object",
    "properties": {
        "description": {
            "type": "string",
            "example": "Foo Bar"
        }
    }
}

specialty_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
        },
        **specialty_minimal["properties"], "created_at": {
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
        "name": "specialties",
    }]
}

post_specialty = {
    **tags, "summary": "Create specialty",
    "description": "Create a new specialty",
    "opeartionId": "post_specialty",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": specialty_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Specialty"),
        "400": validation_response_400,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_specialties = {
    **tags, "summary":
    "Load specialties",
    "description":
    "Filter and load specialties with pagination",
    "opeartionId":
    "get_specialties",
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
        "name": "description",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": list_response_200("Specialty"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_specialty_by_id = {
    **tags, "summary":
    "Load a specialty",
    "description":
    "load specialty by id",
    "opeartionId":
    "get_specialty_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "specialty_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Specialty"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_specialty = {
    **tags, "summary":
    "Update specialty",
    "description":
    "update a specialty using id",
    "opeartionId":
    "put_specialty",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "specialty_id",
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
                "schema": specialty_minimal
            }
        }
    },
    "responses": {
        "200": updated_200("Specialty"),
        "400": validation_response_400,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_specialty = {
    **tags, "summary":
    "Delete specialty",
    "description":
    "update a specialty using id",
    "opeartionId":
    "delete_specialty",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "specialty_id",
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
