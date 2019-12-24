from factory.storage.registry import field_registry

fields = [
    v.get_json_schema() for v in field_registry.registry.values()
]


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
            "items": {
                "oneOf": fields
            }
        },
        "meta": {
            "type": "object",
            "properties": {
                "unique_together": {
                    "type": "array",
                    "minItems": 1,
                    "items": [
                        {
                            "type": "array",
                            "minItems": 2,
                            "items": [
                                {"type": "string", "minLength": 2, "maxLength": 128}
                            ]
                        }
                    ]
                }
            }
        }
    },
    "additionalProperties": False,
    "required": ["name", "key", "fields"]
}


example_data = {
    "name": "Foo",
    "key": {"name": "keyfield", "type": "integer"},
    "fields": [
        {"name": "sf", "type": "string", "max_length": 200}
    ]
}