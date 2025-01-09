from django.db import models
from ..base_model import AbstractBaseModel

class Article(AbstractBaseModel):
    title = models.CharField(max_length=50)
    contents = models.TextField()
    link = models.CharField(max_length=100)
    category = models.ForeignKey('article.Category', on_delete=models.CASCADE, related_name='articles')

    class Meta:
        db_table = "article"

    def __str__(self):
        return self.title
