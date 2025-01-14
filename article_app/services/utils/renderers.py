from rest_framework.renderers import JSONRenderer
from inflection import camelize

class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        def to_camel_case(data):
            if isinstance(data, dict):
                return {camelize(key, uppercase_first_letter=False): to_camel_case(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [to_camel_case(item) for item in data]
            return data

        if isinstance(data, (dict, list)):
            data = to_camel_case(data)

        return super().render(data, accepted_media_type, renderer_context)
