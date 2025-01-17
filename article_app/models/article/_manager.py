from django.db import models
from ._queryset import ArticleQuerySet

class ArticleManager(models.Manager.from_queryset(ArticleQuerySet)):
    pass