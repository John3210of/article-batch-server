from rest_framework import serializers
from article_app.models import Article
from article_app.models import Category

class ArticleSerializer(serializers.ModelSerializer):
    """
    Article 모델에 대한 Serializer입니다.
    """
    category_title = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Article
        fields = ['id', 'title', 'contents', 'link', 'category_id', 'category_title']

    def create(self, validated_data):
        category_title = validated_data.pop('category_title', None)
        if category_title:
            try:
                category = Category.objects.get(title=category_title)
                validated_data['category_id'] = category.id
            except Category.DoesNotExist:
                raise serializers.ValidationError({
                    "category_title": f"Category with the name '{category_title}' does not exist."
                })
        return Article.objects.create(**validated_data)