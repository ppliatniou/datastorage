from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from utils.parsers import JSONSchemaParser


class JSONSchemaViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    parser_classes = (JSONSchemaParser,)
    serializer_class = None
    json_schema = None
    
    def get_json_schema(self):
        if self.json_schema is None:
            raise ValueError("Json schema should be defined")
        return self.json_schema
    
    def get_parsers(self):
        if len(self.parser_classes) != 1:
            raise ValueError("List parser_classes should countain only one parser")
        return [self.parser_classes[0](self.get_json_schema())]
