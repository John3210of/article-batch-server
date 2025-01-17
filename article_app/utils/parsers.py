from rest_framework.parsers import JSONParser
import re

class CamelCaseJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        def to_snake_case(camel_str):
            """Convert CamelCase to snake_case"""
            return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

        def convert_keys(data):
            """Recursively convert keys of dict or list"""
            if isinstance(data, dict):
                return {to_snake_case(k): convert_keys(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [convert_keys(item) for item in data]
            return data

        # Parse the input data
        data = super().parse(stream, media_type, parser_context)
        return convert_keys(data)
