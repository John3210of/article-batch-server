from django.db import models
from ._queryset import CategoryQuerySet

class ArticleManager(models.Manager):
    def get_queryset(self):
        """기본 QuerySet을 커스텀 QuerySet으로 변경"""
        return CategoryQuerySet(self.model, using=self._db)