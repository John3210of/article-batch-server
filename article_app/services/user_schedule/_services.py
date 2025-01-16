from article_app.models import UserSchedule
from article_app.serializers import UserScheduleSerializer
from article_app.services.utils.service_utils import create_response, handle_unexpected_error

class UserScheduleService:
    @staticmethod
    def create_or_replace_user_schedule(data):
        """
        새로운 UserSchedule을 생성하거나 기존 데이터를 대체합니다.
        """
        try:
            serializer = UserScheduleSerializer(data=data)
            if not serializer.is_valid():
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=serializer.errors,
                    status_code=400
                )
            
            user_id = serializer.validated_data['user_id']
            user_email = serializer.validated_data['user_email']
            schedules = serializer.validated_data['schedules']

            UserSchedule.objects.filter(user_id=user_id).delete()

            schedule_objects = [
                UserSchedule(user_id=user_id, user_email=user_email, day_of_week=day)
                for day in schedules
            ]
            UserSchedule.objects.bulk_create(schedule_objects)
            response_serializer = UserScheduleSerializer(schedule_objects, many=True)
            return create_response(data=response_serializer.data, status_code=201)

        except Exception as e:
            return handle_unexpected_error(e, "create_or_replace_user_schedule")

    @staticmethod
    def list_all_schedules():
        """
        모든 User의 Schedule를 조회합니다.
        """
        try:
            queryset = UserSchedule.objects.all()
            serializer = UserScheduleSerializer(queryset, many=True)
            return create_response(data=serializer.data)
        except Exception as e:
            return handle_unexpected_error(e, "list_all_schedules")

    @staticmethod
    def retrieve_user_schedule_by_id(user_id):
        """
        특정 user_id의 Schedule을 조회합니다.
        """
        try:
            schedules = UserSchedule.objects.filter(user_id=user_id)
            schedule_days = [schedule.day_of_week for schedule in schedules]
            response_data = {
                "user_id": user_id,
                "schedules": schedule_days
            }
            return create_response(data=response_data)

        except Exception as e:
            return handle_unexpected_error(e, "retrieve_user_schedule_by_id")
