import jsonschema

from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser


class JSONSchemaParser(JSONParser):
    
    def __init__(self, json_schema, *args, **kwargs):
        super(JSONSchemaParser, self).__init__(*args, **kwargs)
        self.json_schema = json_schema
    
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(
            stream,
            media_type,
            parser_context
        )
        
        try:
            jsonschema.validate(
                instance=data,
                schema=self.json_schema.json
            )
        except jsonschema.ValidationError as e:
            raise ParseError(detail=e.message)
        else:
            return data
