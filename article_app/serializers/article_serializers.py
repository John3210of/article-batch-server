from rest_framework import serializers
from article_app.models import Article, Category


class ArticleSerializer(serializers.ModelSerializer):
    """
    Article 모델에 대한 Serializer입니다.
    """
    category_title = serializers.CharField(write_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'contents', 'link', 'category_id', 'category_title']

    def validate(self, data):
        category_title = data.pop('category_title', None)
        if category_title:
            try:
                category = Category.objects.get(title=category_title)
                data['category_id'] = category.id
            except Category.DoesNotExist:
                raise serializers.ValidationError({
                    "category_title": f"Category with the name '{category_title}' does not exist."
                })
        return data