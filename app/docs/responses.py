def unique_entity_200(schema):
    """
    Create doc response 200
    """
    return {
        "description": "referenced entity",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": f"#/components/schemas/{schema}"
                }
            }
        }
    }


def created_201(schema):
    """
    Create doc response 204
    """
    return {
        "description": "successful operation",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": f"#/components/schemas/{schema}"
                }
            }
        }
    }


updated_200 = created_201

validation_response_400 = {
    "description": "inconsistent request",
    "content": {
        "application/json": {
            "schema": {
                "$ref": "#/components/schemas/ValidationResponse"
            }
        }
    }
}

unauthenticated_user_401 = {
    "description": "required to be authenticated",
    "content": {
        "application/json": {
            "schema": {
                "$ref": "#/components/schemas/SimpleMessageResponse"
            }
        }
    }
}

not_authorized_403 = {
    "description": "without authorization to perform this action",
    "content": {
        "application/json": {
            "schema": {
                "$ref": "#/components/schemas/SimpleMessageResponse"
            }
        }
    }
}

entity_not_found_404 = {
    "description": "entity referenced passed not found",
    "content": {
        "application/json": {
            "schema": {
                "$ref": "#/components/schemas/SimpleMessageResponse"
            }
        }
    }
}


def list_response_200(schema):
    """
    create docs response with list
    """
    return {
        "description": "list with result of operation",
        "content": {
            "application/json": {
                "schema": {
                    "type": "array",
                    "items": {
                        "$ref": f"#/components/schemas/{schema}"
                    }
                }
            }
        }
    }


not_content_success_204 = {
    "description": "successful but without content",
}
