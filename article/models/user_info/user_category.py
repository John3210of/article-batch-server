from django.db import models
from ..base_model import AbstractBaseModel

class UserCategory(AbstractBaseModel):
    user_email = models.EmailField()
    category = models.ForeignKey('article.Category', on_delete=models.CASCADE, related_name='user_categories')
    is_activated = models.BooleanField(default=True)
    sent_mail_count = models.BigIntegerField(default=0)

    class Meta:
        db_table = "user_category"

    def __str__(self):
        return f"{self.user_email} - {self.category.title}"
