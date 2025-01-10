from inflection import camelize
from rest_framework import serializers

class BaseResponseSerializer(serializers.Serializer):
    """
    공통 응답 구조를 위한 Serializer.
    모든 API 응답은 이 구조를 따릅니다.
    """
    success = serializers.BooleanField(default=True)
    errorCode = serializers.CharField(allow_null=True, required=False, default=None)
    data = serializers.JSONField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        def convert_keys_to_camel_case(data):
            if isinstance(data, dict):
                return {camelize(key, uppercase_first_letter=False): convert_keys_to_camel_case(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_keys_to_camel_case(item) for item in data]
            return data

        return convert_keys_to_camel_case(representation)
