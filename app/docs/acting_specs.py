from .responses import created_201, updated_200, \
    validation_response_422, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

acting_minimal = {
    "type": "object",
    "properties": {
        "professional_id": {
            "type": "integer",
            "example": 1
        },
        "clinic_id": {
            "type": "integer",
            "example": 2
        },
        "specialty_id": {
            "type": "integer",
            "example": 3
        },
    }
}

acting_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
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
        **acting_minimal["properties"], "created_at": {
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
        "name": "actuations",
    }]
}

post_acting = {
    **tags, "summary": "Create acting",
    "description": "Create a new acting",
    "operationId": "post_acting",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": acting_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Acting"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_actuations = {
    **tags, "summary":
    "Load actuations",
    "description":
    "Filter and load actuations with pagination",
    "operationId":
    "get_actuations",
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
        "name": "professional_id",
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
        "name": "specialty_id",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": list_response_200("Acting"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_acting_by_id = {
    **tags, "summary":
    "Load a acting",
    "description":
    "load acting by id",
    "operationId":
    "get_acting_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "acting_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Acting"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_acting = {
    **tags, "summary":
    "Update acting",
    "description":
    "update a acting using id",
    "operationId":
    "put_acting",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "acting_id",
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
                "schema": acting_minimal
            }
        }
    },
    "responses": {
        "200": updated_200("Acting"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_acting = {
    **tags, "summary":
    "Delete acting",
    "description":
    "update a acting using id",
    "operationId":
    "delete_acting",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "acting_id",
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
