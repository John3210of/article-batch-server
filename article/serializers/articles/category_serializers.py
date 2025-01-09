from rest_framework import serializers
from article.models.articles.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','version']
