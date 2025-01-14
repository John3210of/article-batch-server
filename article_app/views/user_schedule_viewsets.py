from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from article_app.services.user_schedule._services import UserScheduleService
from drf_yasg import openapi
from inflection import underscore

class UserScheduleViewSet(viewsets.ViewSet):
    """
    UserSchedule 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "userEmail": openapi.Schema(type=openapi.TYPE_STRING, description="User's email address"),
                "schedules": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="List of day of week"
                )
            },
            required=["userEmail", "schedules"]
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
            200: "List of all user schedules",
            400: "Bad request"
        }
    )
    def list(self, request, *args, **kwargs):
        """
        모든 User의 Schedule를 조회합니다.
        """
        return UserScheduleService.list_all_schedules()

    @swagger_auto_schema(
        tags=["User Schedule API"],
        responses={
            200: "Schedules for a specific user",
            400: "Bad request",
            404: "Not found"
        }
    )
    def retrieve(self, request, user_email=None):
        """
        특정 User의 schedule을 조회합니다.
        #TODO : id로 조회기능은 불가능하나, swagger에 노출되는 것 수정할 예정입니다.
        """
        return UserScheduleService.retrieve_user_schedule_by_email(user_email)
