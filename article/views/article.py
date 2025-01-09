from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from article.models.articles.category import Category
from article.serializers.articles.category_serializers import CategorySerializer
from article.serializers.base_serializers import BaseResponseSerializer


class CategoryListView(APIView):
    """
    모든 Category를 조회하는 API
    """

    def get(self, request, *args, **kwargs):
        try:
            # Category 데이터 조회 및 직렬화
            categories = Category.objects.all()
            serialized_data = CategorySerializer(categories, many=True).data

            response_serializer = BaseResponseSerializer(data={
                "success": True,
                "errorCode": None,
                "data": serialized_data
            })

            # 검증 및 응답 반환
            response_serializer.is_valid(raise_exception=True)
            return Response(response_serializer.validated_data)

        except ValidationError as e:
            response_serializer = BaseResponseSerializer(data={
                "success": False,
                "errorCode": "ValidationError",
                "data": None
            })
            response_serializer.is_valid(raise_exception=True)
            return Response(response_serializer.validated_data, status=400)

        except Exception as e:
            response_serializer = BaseResponseSerializer(data={
                "success": False,
                "errorCode": "ServerError",
                "data": None
            })
            response_serializer.is_valid(raise_exception=True)
            return Response(response_serializer.validated_data, status=500)
