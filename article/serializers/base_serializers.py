from rest_framework import serializers

class BaseResponseSerializer(serializers.Serializer):
    """
    공통 응답 구조를 위한 Serializer.
    모든 API 응답은 이 구조를 따릅니다.
    """
    success = serializers.BooleanField()
    errorCode = serializers.CharField(allow_null=True, required=False)
    data = serializers.JSONField()
