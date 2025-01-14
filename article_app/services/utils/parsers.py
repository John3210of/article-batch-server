import re
from rest_framework.parsers import JSONParser

class CamelCaseJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        def to_snake_case(camel_str):
            return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

        data = super().parse(stream, media_type, parser_context)
        if isinstance(data, dict):
            data = {to_snake_case(k): v for k, v in data.items()}
        return data
