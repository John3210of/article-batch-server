from rest_framework import serializers
from article.models.user_info.user_category import UserCategory

class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ['id', 'user_email', 'category', 'is_activated', 'sent_mail_count']

class UserCategoryCreateSerializer(serializers.ModelSerializer):
    userEmail = serializers.EmailField(source="user_email", required=True)
    categoryId = serializers.IntegerField(source="category", required=True)

    class Meta:
        model = UserCategory
        fields = ['userEmail', 'categoryId']
