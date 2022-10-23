from .responses import auth_200, unauthenticated_401, auth_only_access_token_200

credentials = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "example": "health10111"
        },
        "password": {
            "type": "string",
            "example": "*********"
        },
    }
}

tags = {
    "tags": [{
        "name": "auth",
    }]
}

signin = {
    **tags, "summary":
    "Perform login",
    "description":
    "User login",
    "opeartionId":
    "auth_signin",
    "parameters": [{
        "name": "remember_me",
        "in": "query",
        "required": False,
        "schema": {
            "type": "boolean",
            "default": False
        }
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": credentials
            }
        }
    },
    "responses": {
        "200": auth_200(),
        "401": unauthenticated_401,
    }
}

refresh_token = {
    **tags, "summary": "Refresh token",
    "description": "refresh token that go expire",
    "opeartionId": "refresh_token",
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": auth_only_access_token_200(),
        "401": unauthenticated_401,
    }
}

restore_session = {
    **tags, "summary": "Restore session",
    "description": "Restore session with session token",
    "opeartionId": "restore_session",
    "security": [{
        "BearerAuthSession": []
    }],
    "responses": {
        "200": auth_only_access_token_200(),
        "401": unauthenticated_401,
    }
}
