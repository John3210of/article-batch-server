from rest_framework import serializers
from article_app.models.user_category._models import UserCategory

class UserCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    category_title = serializers.CharField(source='category.title')

    class Meta:
        model = UserCategory
        fields = ['id', 'user_id', 'user_email', 'category_id', 'category_title', 'is_activated', 'last_mailed_article_id']

class UserCategoryCreateSerializer(serializers.ModelSerializer):
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    class Meta:
        model = UserCategory
        fields = ['user_id', 'user_email', 'category_ids']