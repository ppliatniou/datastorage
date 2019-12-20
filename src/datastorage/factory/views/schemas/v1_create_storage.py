json = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 255},
        "key": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "minLength": 1, "maxLength": 128},
                        "type": {"type": "string", "enum": ["integer", "long"]}
                    },
                    "required": ["name", "type"]
                },
                {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "minLength": 1, "maxLength": 128},
                        "type": {"type": "string", "enum": ["string"]},
                        "max_length": {"type": "integer", "minimum": 1, "maximum": 1024}
                    },
                    "required": ["name", "type", "max_length"]
                }
            ]
        },
        "fields": {
            "type": "array",
            "minItems": 1,
            "items": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "minLength": 2, "maxLength": 128},
                            "type": {"type": "string", "enum": ["integer", "long"]},
                            "default": {"type": "integer", "minimum": 0}
                        },
                        "required": ["name", "type"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "minLength": 2, "maxLength": 128},
                            "type": {"type": "string", "value": "string"},
                            "max_length": {"type": "integer", "minimum": 1, "maximum": 1024},
                            "default": {"type": "string", "minLength": 0}
                        },
                        "required": ["name", "type"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "minLength": 2, "maxLength": 128},
                            "type": {"type": "string", "value": "text"},
                            "default": {"type": "string", "minLength": 0}
                        },
                        "required": ["name", "type"]
                    }
                ]
        },
        "indexes": {
            "type": "object",
            "properties": {
                "unique": {
                    "type": "array",
                    "minItems": 1,
                    "items": [
                        {"type": "string", "minLength": 2, "maxLength": 128}
                    ]
                }
            }
        }
    },
    "required": ["name", "key", "fields"]
}


example_data = {
    "name": "Foo",
    "key": {"name": "keyfield", "type": "integer"},
    "fields": [
        {"name": "sf", "type": "string", "max_length": 200}
    ]
}