from django.db import models
from ._queryset import CategoryQuerySet

class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    pass