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
    Create doc response 201
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


def auth_200():
    """
    Create doc response successfull auth
    """
    return {
        "description": "successful operation",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "access_token": {
                            "type":
                            "string",
                            "example":
                            # pylint: disable=line-too-long
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
                        },
                        "session_token": {
                            "type":
                            "string",
                            "example":
                            # pylint: disable=line-too-long
                            "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.VFb0qJ1LRg_4ujbZoRMXnVkUgiuKq5KxWqNdbKq_G9Vvz-S1zZa9LPxtHWKa64zDl2ofkT8F6jBt_K4riU-fPg"
                        }
                    }
                }
            }
        }
    }


def auth_only_access_token_200():
    """
    Create doc response successfull auth
    """
    return {
        "description": "successful operation",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "access_token": {
                            "type":
                            "string",
                            "example":
                            # pylint: disable=line-too-long
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
                        }
                    }
                }
            }
        }
    }


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

unauthenticated_401 = {
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
