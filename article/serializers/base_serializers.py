from rest_framework import serializers

class BaseResponseSerializer(serializers.Serializer):
    """
    공통 응답 구조를 위한 Serializer.
    모든 API 응답은 이 구조를 따릅니다.
    기본적으로 성공(success=True)으로 설정됩니다.
    """
    success = serializers.BooleanField(default=True)
    errorCode = serializers.CharField(allow_null=True, required=False, default=None)
    data = serializers.JSONField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'success' not in representation:
            representation['success'] = True
        if 'errorCode' not in representation:
            representation['errorCode'] = None

        return representation
