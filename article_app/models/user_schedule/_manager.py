from django.db import models
from ._queryset import UserScheduleQuerySet

class UserScheduleManager(models.Manager):
    def get_queryset(self):
        """기본 QuerySet을 커스텀 QuerySet으로 변경"""
        return UserScheduleQuerySet(self.model, using=self._db)