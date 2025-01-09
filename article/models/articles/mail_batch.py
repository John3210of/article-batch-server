from django.db import models
from ..base_model import AbstractBaseModel
from ...enums.mail_status import MailStatus

class MailBatch(AbstractBaseModel):
    user_email = models.EmailField()
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE, related_name='mail_batches')
    reservation_date = models.DateField()
    status = models.CharField(
        max_length=100,
        choices=MailStatus.choices(),
        default=MailStatus.CREATED.value,
    )

    class Meta:
        db_table = "mail_batch"

    def __str__(self):
        return f"{self.user_email} - {self.article.title} - {self.status}"
