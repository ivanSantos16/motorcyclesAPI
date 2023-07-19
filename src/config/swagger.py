template = {
    "swagger": "2.0",
    "info": {
        "title": "Motorcycles API",
        "description": "API for detailed data about motorcycles",
        "version": "1.0",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "Ivan Santos",
            "url": "https://ivansantos16.github.io",
            "email": "ivan.rafa.16@gmail.com",
        },
        "termsOfService": "https://ivansantos16.github.io",
    },
    "basePath": "/api/v1",
    "tags": [
        {"name": "Authentication", "description": "Authentication operations to Motorcycles API"},
        {"name": "Motorcycle", "description": "Operations with motorcycles"},
    ],
        
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": ">- JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}' , please enter the token with the 'Bearer ' prefix.",
        }
    },
    "definitions": {
        "APIResponse": {
            "type": "object",
            "properties": {
                "status": {"type": "integer", "format": "int32", "example": 200},
                "message": {"type": "string", "example": "Motorcycle added successfully"},
                "data": {"type": "object"},
            },
        },
        "APIResponseMetadata": {
            "type": "object",
            "properties": {
                "status": {"type": "integer", "format": "int32", "example": 200},
                "message": {"type": "string", "example": "Motorcycle info retrieved sucessfully"},
                "data": {"type": "object"},
                "metadata": {"$ref": "#/definitions/Metadata"},
            },
        },
        "Metadata": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "format": "int32", "example": 2},
                "pages": {"type": "integer", "format": "int32", "example": 5},
                "prev_page": {"type": "integer", "format": "int32", "example": 1},
                "next_page": {"type": "integer", "format": "int32", "example": 3},
                "has_next": {"type": "boolean", "example": True},
                "has_prev": {"type": "boolean", "example": True}
            },
        },
        "DateTime": {"type": "string", "format": "date-time"},
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "format": "int32"},
                "username": {"type": "string", "example": "user"},
                "email": {"type": "string", "example": "user@email.com"},
                "password": {"type": "string"},
                "created_at": {"$ref": "#/definitions/DateTime"},
                "updated_at": {"$ref": "#/definitions/DateTime"},
            },
        },
        "Stats": {
            "type": "object",
            "properties": {
                "test": {"$ref": "#/definitions/Motorcycle.niv"},
                "visits": {"type": "integer", "format": "int32"},
                "url": {"type": "string", "example": "http://localhost:5000/api/v1/motorcycles/1"},
                "niv": {"type": "string", "example": "JH2SC59A0DK000001"},
                "short_url": {"type": "string", "example": "aW0"},
            },
        },
        "Motorcycle": {
            "type": "object",
            "properties": {
                "niv": {"type": "string", "example": "JH2SC59A0DK000001"},
                "brand": {"type": "string", "example": "Honda"},
                "model": {"type": "string", "example": "CBR 1000RR"},
                "year": {"type": "integer", "format": "int32", "example": 2019},
                "category": {"type": "string", "example": "Sport"},
                "rating": {"type": "number", "format": "float", "example": 4.5},
                "displacement": {"type": "integer", "format": "int32", "example": 999, "description": "In ccm"},
                "power": {"type": "integer", "format": "int32", "example": 189, "description": "In hp"},
                "torque": {"type": "integer", "format": "int32", "example": 11, "description": "In Nm"},
                "engine_cylinders": {"type": "string", "example": "4"},
                "engine_strokes": {"type": "string", "example": "4-strokes"},
                "gearbox": {"type": "string", "example": "6-speed"},
                "bore": {"type": "number", "format": "integer", "example": 76, "description": "In mm"},
                "stroke": {"type": "number", "format": "float", "example": 55.5, "description": "In mm"},
                "transmission_type": {"type": "string", "example": "Chain"},
                "front_brakes": {"type": "string", "example": "Double disc"},
                "rear_brakes": {"type": "string", "example": "Single disc"},
                "front_suspension": {"type": "string", "example": "Telescopic fork"},
                "rear_suspension": {"type": "string", "example": "Swingarm"},
                "front_tire": {"type": "string", "example": "120/70-ZR17"},
                "rear_tire": {"type": "string", "example": "190/50-ZR17"},
                "dry_weight": {"type": "integer", "format": "int32", "example": 201, "description": "In kg"},
                "wheelbase": {"type": "integer", "format": "int32", "example": 1405, "description": "In mm"},
                "fuel_capacity": {"type": "integer", "format": "int32", "example": 16, "description": "In liters"},
                "fuel_system": {"type": "string", "example": "Injection"},
                "fuel_control": {"type": "string", "example": "DOHC"},
                "seat_height": {"type": "integer", "format": "float", "example": 820.3, "description": "In mm"},
                "cooling_system": {"type": "string", "example": "Liquid"},
                "color_options": {"type": "string", "example": "Red, Black, White"},
            },
        },
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",  # json version of the documentation
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",  # static path to generate the css of swagger
    "swagger_ui": True,
    "specs_route": "/",  # url to access the swagger ui
}
