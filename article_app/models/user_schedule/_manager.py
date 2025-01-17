from django.db import models
from ._queryset import UserScheduleQuerySet

class UserScheduleManager(models.Manager.from_queryset(UserScheduleQuerySet)):
    pass
