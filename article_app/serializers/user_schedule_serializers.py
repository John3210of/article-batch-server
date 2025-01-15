from rest_framework import serializers
from article_app.models.user_schedule._models import UserSchedule
from article_app.enums.day_of_week import DayOfWeek

class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSchedule
        fields = ['id', 'user_id', 'user_email', 'day_of_week']

class UserScheduleCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    user_email = serializers.EmailField(required=True)
    schedules = serializers.ListField(
        child=serializers.ChoiceField(choices=DayOfWeek.choices()),
        required=True
    )
