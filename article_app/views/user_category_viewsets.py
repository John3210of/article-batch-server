from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from article_app.services.user_category._services import UserCategoryService
from drf_yasg import openapi

class UserCategoryViewSet(viewsets.ViewSet):
    """
    UserCategory 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        tags=["User Category API"],
        responses={
            200: "List of User Categories",
            400: "Invalid Request"
        },
    )
    def list(self, request, *args, **kwargs):
        """
        모든 UserCategory를 조회합니다.
        """
        return UserCategoryService.list_all_user_categories()

    @swagger_auto_schema(
        tags=["User Category API"],
        responses={
            200: "User Categories for given user_email",
            400: "Invalid Request",
            404: "Not Found"
        },
    )
    def retrieve(self, request, pk=None):
        """
        특정 사용자의 구독중인 UserCategory를 userId를 통해 조회합니다.
        """
        user_id = pk
        return UserCategoryService.retrieve_user_categories_by_user_id(user_id)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "userId": openapi.Schema(type=openapi.TYPE_STRING, description="User's ID"),
                "userEmail": openapi.Schema(type=openapi.TYPE_STRING, description="User's email address"),
                "categoryIds": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of category IDs"
                )
            },
            required=["userId","userEmail","categoryIds"]
        ),
        responses={
            201: "User Categories Created/Updated",
            400: "Invalid Request"
        },
        tags=["User Category API"]
    )
    def create(self, request, *args, **kwargs):
        """
        새로운 UserCategory를 생성하거나 업데이트합니다.
        """
        return UserCategoryService.create_or_update_user_categories(request.data)
