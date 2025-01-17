from django.db import models
from article_app.models.base_model import AbstractBaseModel
from ._manager import CategoryManager
class Category(AbstractBaseModel):
    title = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    link = models.CharField(max_length=100)
    
    objects = CategoryManager()
    
    class Meta:
        db_table = "category"

    def __str__(self):
        return self.title
