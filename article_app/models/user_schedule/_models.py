from django.db import models
from article_app.models.base_model import AbstractBaseModel
from article_app.enums.day_of_week import DayOfWeek
from ._manager import UserScheduleManager

class UserSchedule(AbstractBaseModel):
    user_id = models.BigIntegerField()
    user_email = models.EmailField()
    day_of_week = models.CharField(
        max_length=3,
        choices=DayOfWeek.choices(),
    )

    objects = UserScheduleManager()

    class Meta:
        db_table = "user_schedule"

    def __str__(self):
        return f"{self.user_email} - {self.day_of_week}"
