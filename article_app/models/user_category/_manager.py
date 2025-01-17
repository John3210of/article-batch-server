from django.db import models
from ._queryset import UserCategoryQuerySet

class UserCategoryManager(models.Manager.from_queryset(UserCategoryQuerySet)):
    pass
