from rest_framework import serializers
from article.models.articles.article import Article
from article.models.articles.category import Category

class BulkArticleSerializer(serializers.ListSerializer):
    """
    여러 개의 Article 객체를 직렬화하거나 역직렬화합니다.
    """
    def create(self, validated_data):
        articles = []
        for item in validated_data:
            category_title = item.pop('category_title', None)
            if category_title:
                try:
                    category = Category.objects.get(title=category_title)
                    item['category_id'] = category
                except Category.DoesNotExist:
                    raise serializers.ValidationError({
                        "category_title": f"Category with the name '{category_title}' does not exist."
                    })
            articles.append(Article(**item))
        return Article.objects.bulk_create(articles)

class ArticleSerializer(serializers.ModelSerializer):
    """
    Article 모델에 대한 Serializer입니다.
    """
    category_title = serializers.CharField(write_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'contents', 'link', 'category_id', 'category_title']
        list_serializer_class = BulkArticleSerializer

    def validate_title(self, value):
        """
        제목의 유효성을 검사합니다.
        """
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_link(self, value):
        """
        링크의 유효성을 검사합니다.
        """
        if not value.startswith("http"):
            raise serializers.ValidationError("Link must be a valid URL starting with http or https.")
        return value

    def to_internal_value(self, data):
        """
        category_title을 category_id로 변환하여 내부 데이터로 변환합니다.
        """
        if 'category_title' not in data:
            raise serializers.ValidationError({"category_title": "This field is required."})

        category_title = data.get('category_title')
        try:
            category = Category.objects.get(title=category_title)
            data['category_id'] = category.id
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category_title": "Category with this name does not exist."})
        
        return super().to_internal_value(data)
    def create(self, validated_data):
        """
        Create 메서드에서 category_title을 제거하고 category_id를 사용해 객체를 생성합니다.
        """
        validated_data.pop('category_title', None)  # category_title 제거
        return Article.objects.create(**validated_data)