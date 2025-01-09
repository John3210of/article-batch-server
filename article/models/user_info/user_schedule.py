from django.db import models
from article.models.base_model import AbstractBaseModel
from article.enums.day_of_week import DayOfWeek
class UserSchedule(AbstractBaseModel):
    user_email = models.EmailField()
    day_of_week = models.CharField(
        max_length=3,
        choices=DayOfWeek.choices(),
    )

    class Meta:
        db_table = "user_schedule"

    def __str__(self):
        return f"{self.user_email} - {self.day_of_week}"
