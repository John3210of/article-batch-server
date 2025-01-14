from rest_framework import serializers
from article_app.models.user_category._models import UserCategory

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