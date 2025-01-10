from rest_framework import viewsets, status
from rest_framework.response import Response
from article.models.articles.category import Category
from article.serializers.articles.category_serializers import CategorySerializer
from article.serializers.base_serializers import BaseResponseSerializer
from drf_yasg.utils import swagger_auto_schema

class CategoryViewSet(viewsets.ViewSet):
    """
    Category 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        tags=["Category API"],
        responses={
            200: BaseResponseSerializer,
            400: BaseResponseSerializer,
            404: BaseResponseSerializer,
        },
    )
    def retrieve(self, request, pk=None):
        """
        특정 Category를 조회합니다.
        """
        if not pk:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "Category ID is required"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=pk)
            serialized_data = CategorySerializer(category).data
            response_data = {
                "data": serialized_data
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Category not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Category API"], responses={200: BaseResponseSerializer})
    def list(self, request):
        """
        모든 Category를 조회합니다.
        """
        categories = Category.objects.all()
        serialized_data = CategorySerializer(categories, many=True).data
        response_data = {
            "data": serialized_data
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={201: BaseResponseSerializer, 400: BaseResponseSerializer},
        tags=["Category API"]
    )
    def create(self, request):
        """
        새로운 Category를 생성합니다.
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "data": serializer.data
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_201_CREATED)

        response_data = {
            "success": False,
            "errorCode": "ERR400",
            "data": serializer.errors
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={200: BaseResponseSerializer, 400: BaseResponseSerializer, 404: BaseResponseSerializer},
        tags=["Category API"]
    )
    def partial_update(self, request, pk=None):
        """
        특정 Category를 부분 업데이트합니다.
        """
        if not request.data:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "Request body is empty"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "data": serializer.data
                }
                return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": serializer.errors
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        except Category.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Category not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)
