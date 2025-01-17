from django.db import models
from ._queryset import MailBatchQuerySet

class MailBatchManager(models.Manager.from_queryset(MailBatchQuerySet)):
    pass