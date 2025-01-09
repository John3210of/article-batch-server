from django.db import models
from ..base_model import AbstractBaseModel

class Category(AbstractBaseModel):
    title = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    link = models.CharField(max_length=100)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.title
