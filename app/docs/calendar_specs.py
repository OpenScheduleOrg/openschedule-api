from .responses import unauthenticated_401, not_authorized_403, list_response_200

tags = {
    "tags": [{
        "name": "calendar",
    }]
}

get_specialties_availables = {
    **tags, "summary":
    "Obtain clinic specialties with available schedules",
    "description":
    "Obtain clinic specialties with available schedules",
    "operationId":
    "get_specialty_availables",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_id",
        "in": "query",
        "required": True,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": list_response_200("Specialty"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_free_days = {
    **tags, "summary":
    "Return next days with availables schedules",
    "description":
    "Return next x days with availables schedules",
    "operationId":
    "get_free_days",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "clinic_id",
        "in": "query",
        "required": True,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "specialty_id",
        "in": "query",
        "required": True,
        "schema": {
            "type": "integer",
        }
    }, {
        "name": "num_days",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
            "default": 10
        }
    }, {
        "name": "start_date",
        "in": "query",
        "required": True,
        "schema": {
            "type": "string",
            "format": "date",
        }
    }, {
        "name": "first_day_startime",
        "in": "query",
        "required": False,
        "schema": {
            "type": "date",
        }
    }],
    "responses": {
        "200": {
            "description": "list with result of operation",
            "content": {
                "application/json": {
                    "schema": {
                        "type":
                        "array",
                        "items": {
                            "oneOf": [{
                                "type": "string",
                                "format": "date",
                                "example": "2022-12-20"
                            }, {
                                "type": "string",
                                "format": "date",
                                "example": "2022-12-21"
                            }, {
                                "type": "string",
                                "format": "date",
                                "example": "2022-12-22"
                            }]
                        },
                        "examples": [
                            "2022-12-20", "2022-12-21", "2022-12-22",
                            "2022-12-22"
                        ],
                    }
                }
            }
        },
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}
