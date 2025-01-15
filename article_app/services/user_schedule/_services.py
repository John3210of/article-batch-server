from article_app.models.user_schedule._models import UserSchedule
from article_app.serializers.user_schedule_serializers import UserScheduleCreateSerializer, UserScheduleSerializer
from article_app.services.utils.service_utils import create_response, handle_unexpected_error

class UserScheduleService:
    @staticmethod
    def create_or_replace_user_schedule(data):
        """
        새로운 UserSchedule을 생성하거나 기존 데이터를 삭제 후 다시 생성합니다.
        """
        try:
            serializer = UserScheduleCreateSerializer(data=data)
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

            created_schedules = [
                UserSchedule.objects.create(user_id=user_id, user_email=user_email, day_of_week=day)
                for day in schedules
            ]

            # 생성된 데이터 반환
            response_serializer = UserScheduleSerializer(created_schedules, many=True)
            return create_response(success=True, data=response_serializer.data, status_code=201)

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
            return create_response(success=True, data=serializer.data, status_code=200)
        except Exception as e:
            return handle_unexpected_error(e, "list_all_schedules")

    @staticmethod
    def retrieve_user_schedule_by_id(user_id):
        """
        특정 user_id의 Schedule을 조회합니다.
        """
        try:
            schedules = UserSchedule.objects.filter(user_id=user_id)
            if not schedules.exists():
                return create_response(
                    success=False,
                    error_code="ERR404",
                    data={"message": "UserSchedule not found"},
                    status_code=404
                )

            schedule_days = [schedule.day_of_week for schedule in schedules]
            response_data = {
                "user_id": user_id,
                "schedules": schedule_days
            }
            return create_response(success=True, data=response_data, status_code=200)

        except Exception as e:
            return handle_unexpected_error(e, "retrieve_user_schedule_by_id")
