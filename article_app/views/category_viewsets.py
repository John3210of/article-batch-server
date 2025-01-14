from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from article_app.services.category._services import CategoryService
from drf_yasg import openapi

class CategoryViewSet(viewsets.ViewSet):
    """
    Category 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        tags=["Category API"]
    )
    def retrieve(self, request, pk=None):
        """
        특정 카테고리를 조회하는 API입니다.
        """
        return CategoryService.get_category_by_id(pk)

    @swagger_auto_schema(
        tags=["Category API"]
    )
    def list(self, request):
        """
        모든 카테고리를 조회하는 API입니다.
        """
        return CategoryService.get_all_categories()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Category title"),
                "version": openapi.Schema(type=openapi.TYPE_STRING, description="Category version"),
                "link": openapi.Schema(type=openapi.TYPE_STRING, description="Category link")
            },
            required=["title", "version", "link"]
        ),
        tags=["Category API"]
    )
    def create(self, request):
        """
        새로운 카테고리를 생성하는 API입니다.
        """
        return CategoryService.create_category(request.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Category title"),
                "version": openapi.Schema(type=openapi.TYPE_STRING, description="Category version"),
                "link": openapi.Schema(type=openapi.TYPE_STRING, description="Category link")
            },
        ),
        tags=["Category API"]
    )
    def partial_update(self, request, pk=None):
        """
        특정 카테고리를 업데이트하는 API입니다.
        """
        return CategoryService.update_category(pk, request.data)
