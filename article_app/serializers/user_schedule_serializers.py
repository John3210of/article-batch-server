from rest_framework import serializers
from article_app.models import UserSchedule

class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSchedule
        fields = ['id', 'user_id', 'user_email', 'day_of_week']