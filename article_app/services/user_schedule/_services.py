from article_app.models import UserSchedule
from article_app.serializers import UserScheduleSerializer
from article_app.services.base._service import BaseService
from article_app.services.utils.service_utils import create_response,exception_handler

class UserScheduleService(BaseService):
    
    @staticmethod
    def list_all_schedules():
        """
        모든 User의 Schedule를 조회합니다.
        """
        return BaseService.get_all_objects(UserSchedule, UserScheduleSerializer)

    @staticmethod
    @exception_handler(method_name="retrieve_user_schedule_by_id")
    def retrieve_user_schedule_by_id(user_id):
        """
        특정 user_id의 Schedule을 조회합니다.
        """
        schedules = UserSchedule.objects.filter(user_id=user_id)
        schedule_days = [schedule.day_of_week for schedule in schedules]
        response_data = {
            "user_id": user_id,
            "schedules": schedule_days
        }
        return create_response(data=response_data)

    @staticmethod
    @exception_handler(method_name="create_or_replace_user_schedule")
    def create_or_replace_user_schedule(data):
        """
        새로운 UserSchedule을 생성하거나 기존 데이터를 대체합니다.
        """
        serializer = UserScheduleSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user_id = validated_data['user_id']
        user_email = validated_data['user_email']
        schedules = validated_data['schedules']

        UserSchedule.objects.filter(user_id=user_id).delete()
        schedule_objects = [
            UserSchedule(user_id=user_id, user_email=user_email, day_of_week=day)
            for day in schedules
        ]
        UserSchedule.objects.bulk_create(schedule_objects)

        response_serializer = UserScheduleSerializer(schedule_objects, many=True)
        return create_response(data=response_serializer.data, status_code=201)

