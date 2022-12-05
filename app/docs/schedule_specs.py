from .responses import created_201, updated_200, \
    validation_response_422, unauthenticated_401, not_authorized_403, \
    list_response_200, unique_entity_200, entity_not_found_404, not_content_success_204

schedule_minimal = {
    "type": "object",
    "properties": {
        "start_date": {
            "type": "string",
            "format": "date",
            "example": "2022-10-24"
        },
        "end_date": {
            "type": "string",
            "format": "date",
            "example": "2023-01-01"
        },
        "start_time": {
            "type": "integer",
            "example": 420
        },
        "end_time": {
            "type": "integer",
            "example": 480
        },
        "max_visits": {
            "type": "integer",
            "example": 3
        },
        "week_day": {
            "type": "integer",
            "example": 4
        },
        "acting_id": {
            "type": "integer",
            "example": 1
        }
    }
}

schedule_model = {
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
        **schedule_minimal["properties"], "created_at": {
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
        "name": "schedules",
    }]
}

post_schedule = {
    **tags, "summary": "Create schedule",
    "description": "Create a new schedule",
    "operationId": "post_schedule",
    "security": [{
        "BearerAuth": []
    }],
    "requestBody": {
        "description": "Any description about body request",
        "content": {
            "application/json": {
                "schema": schedule_minimal
            }
        }
    },
    "responses": {
        "201": created_201("Schedule"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_schedules = {
    **tags, "summary":
    "Load schedules",
    "description":
    "Filter and load schedules with pagination",
    "operationId":
    "get_schedules",
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
        "name": "acting_id",
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
        "name": "professional_id",
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
        "200": list_response_200("Schedule"),
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

get_schedule_by_id = {
    **tags, "summary":
    "Load a schedule",
    "description":
    "load schedule by id",
    "operationId":
    "get_schedule_by_id",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "schedule_id",
        "in": "path",
        "required": False,
        "schema": {
            "type": "integer",
        }
    }],
    "responses": {
        "200": unique_entity_200("Schedule"),
        "404": entity_not_found_404,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

update_schedule = {
    **tags, "summary":
    "Update schedule",
    "description":
    "update a schedule using id",
    "operationId":
    "put_schedule",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "schedule_id",
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
                "schema": schedule_minimal
            }
        }
    },
    "responses": {
        "200": updated_200("Schedule"),
        "422": validation_response_422,
        "401": unauthenticated_401,
        "403": not_authorized_403,
    }
}

delete_schedule = {
    **tags, "summary":
    "Delete schedule",
    "description":
    "update a schedule using id",
    "operationId":
    "delete_schedule",
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [{
        "name": "schedule_id",
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
