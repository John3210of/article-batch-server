from rest_framework import serializers
from article.models.user_info.user_category import UserCategory
from article.models.user_info.user_schedule import UserSchedule
from article.enums.day_of_week import DayOfWeek
class UserCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    category_title = serializers.CharField(source='category.title')

    class Meta:
        model = UserCategory
        fields = ['id','user_email', 'category_id', 'category_title', 'is_activated', 'sent_mail_count']

class UserCategoryCreateSerializer(serializers.ModelSerializer):
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    class Meta:
        model = UserCategory
        fields = ['user_email', 'category_ids']

class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSchedule
        fields = ['id','user_email']

class UserScheduleCreateSerializer(serializers.Serializer):
    user_email = serializers.EmailField(required=True)
    schedules = serializers.ListField(
        child=serializers.ChoiceField(choices=DayOfWeek.choices()),
        required=True
    )
    
    class Meta:
        model = UserSchedule
        fields = ['user_email','schedules']