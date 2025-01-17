from django.db import models
from article_app.models.base_model import AbstractBaseModel
from article_app.enums.mail_status import MailStatus
from ._manager import MailBatchManager
class MailBatch(AbstractBaseModel):
    user_email = models.EmailField()
    article = models.ForeignKey('article_app.Article', on_delete=models.CASCADE, related_name='mail_batches')
    reservation_date = models.DateField()
    status = models.CharField(
        max_length=100,
        choices=MailStatus.choices(),
        default=MailStatus.CREATED.value,
    )
    
    objects = MailBatchManager()
    
    class Meta:
        db_table = "mail_batch"

    def __str__(self):
        return f"{self.user_email} - {self.article.title} - {self.status}"
