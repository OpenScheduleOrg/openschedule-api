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
    "opeartionId":
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
