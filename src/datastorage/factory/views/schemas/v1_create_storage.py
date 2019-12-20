json = {
    "type": "object",
    "properties": {
        "a": {"type": "integer"}
    },
    "required": ["a"]
    # "name": "Product",
    # "properties": {
    #     "name": {
    #         "type": "string",
    #         "required": True
    #     },
    #     "price": {
    #         "type": "number",
    #         "minimum": 0,
    #         "required": True
    #     },
    #     "tags": {
    #         "type": "array",
    #         "items": {"type": "string"}
    #     },
    #     "stock": {
    #         "type": "object",
    #         "properties": {
    #             "warehouse": {"type": "number"},
    #             "retail": {"type": "number"}
    #         }
    #     }
    # }
}

# The JSON Schema above can be used to test the validity of the JSON code below:
example_data = {
    "name": "Foo",
    "price": 123,
    "tags": ["Bar", "Eek"],
    "stock": {
        "warehouse": 300,
        "retail": 20
    }
}