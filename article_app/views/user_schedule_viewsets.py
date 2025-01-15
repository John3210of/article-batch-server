from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from article_app.services.user_schedule._services import UserScheduleService
from drf_yasg import openapi

class UserScheduleViewSet(viewsets.ViewSet):
    """
    UserSchedule 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "userId": openapi.Schema(type=openapi.TYPE_INTEGER, description="User's ID"),  # user_id 추가
                "userEmail": openapi.Schema(type=openapi.TYPE_STRING, description="User's email address"),
                "schedules": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="List of day of week"
                )
            },
            required=["userId", "userEmail", "schedules"]
        ),
        responses={
            201: "User Schedules created or replaced",
            400: "Bad request"
        },
        tags=["User Schedule API"]
    )
    def create(self, request, *args, **kwargs):
        """
        새로운 User schedule을 생성하거나 기존 데이터를 삭제하고 다시 생성합니다.
        """
        return UserScheduleService.create_or_replace_user_schedule(request.data)

    @swagger_auto_schema(
        tags=["User Schedule API"],
        responses={
            200: "Schedules for a specific user by ID",
            400: "Bad request",
            404: "Not found"
        }
    )
    def retrieve(self, request, pk=None):
        """
        특정 User의 schedule을 userID로 조회합니다.
        """
        user_id = pk
        return UserScheduleService.retrieve_user_schedule_by_id(user_id)
        
    @swagger_auto_schema(
            tags=["User Schedule API"],
            responses={
                200: "List of User Schedules",
                400: "Invalid Request"
            },
        )
    def list(self, request, *args, **kwargs):
        """
        모든 User Schedule을 조회합니다.
        """
        return UserScheduleService.list_all_schedules()