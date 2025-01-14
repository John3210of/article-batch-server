from rest_framework import serializers

class BaseResponseSerializer(serializers.Serializer):
    """
    공통 응답 구조를 위한 Serializer.
    현재는 사용하지 않습니다.
    """
    pass
