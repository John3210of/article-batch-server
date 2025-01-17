from django.db import models
from article_app.models.base_model import AbstractBaseModel
from ._manager import ArticleManager
class Article(AbstractBaseModel):
    title = models.CharField(max_length=50)
    contents = models.TextField()
    link = models.CharField(max_length=100)
    category = models.ForeignKey('article_app.Category', on_delete=models.CASCADE, related_name='articles')

    objects = ArticleManager()
    class Meta:
        db_table = "article"

    def __str__(self):
        return self.title
