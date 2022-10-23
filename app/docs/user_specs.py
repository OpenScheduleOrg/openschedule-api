from .responses import created_201, updated_200, \
    validation_response_400, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

user_minimal = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "example": "Foo Bar"
        },
        "username": {
            "type": "string",
            "example": "foobar23"
        },
        "email": {
            "type": "string",
            "example": "foo@bar.yz",
        },
        "password": {
            "type": "string",
            "example": "supersecret"
        },
        "clinic_id": {
            "type": "integer",
            "example": 1
        }
    }
}

user_update = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "example": "Foo Bar"
        },
        "username": {
            "type": "string",
            "example": "foobar23"
        },
        "email": {
            "type": "string",
            "example": "foo@bar.yz",
        },
        "clinic_id": {
            "type": "integer",
            "example": 1
        }
    }
}

user_model = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 10
        },
        **user_minimal["properties"], "created_at": {
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
        "name": "users",
    }]
}

post_user = {
    **tags, "summary": "Create user",
    "description": "Create a new user",
    "opeartionId": "post_user",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": user_minimal
            }
        }
    },
    "responses": {
        "201": created_201("User"),
        "400": validation_response_400,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_users = {
    **tags, "summary":
    "Load users",
    "description":
    "Filter and load users with pagination",
    "opeartionId":
    "get_users",
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
        "200": list_response_200("User"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_user_by_id = {
    **tags, "summary":
    "Load a user",
    "description":
    "load user by id",
    "opeartionId":
    "get_user_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "user_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("User"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_user_by_username = {
    **tags, "summary":
    "Load a user using username",
    "description":
    "load user by username",
    "opeartionId":
    "get_user_by_username",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "user_username",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("User"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_user_by_email = {
    **tags, "summary":
    "Load a user email",
    "description":
    "load user by email",
    "opeartionId":
    "get_user_by_email",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "user_email",
        "in": "path",
        "description": "must be without mask",
        "required": False,
        "schema": {
            "type": "string",
        }
    }],
    "responses": {
        "200": unique_entity_200("User"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_user = {
    **tags, "summary":
    "Update user",
    "description":
    "update a user using id",
    "opeartionId":
    "put_user",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "user_id",
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
                "schema": user_update
            }
        }
    },
    "responses": {
        "200": updated_200("User"),
        "400": validation_response_400,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_user = {
    **tags, "summary":
    "Delete user",
    "description":
    "update a user using id",
    "opeartionId":
    "delete_user",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "user_id",
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
