from rest_framework import serializers
from article_app.models import MailBatch

class MailBatchSerializer(serializers.ModelSerializer):
    """
    Serializer for MailBatch model.
    """

    class Meta:
        model = MailBatch
        fields = ['id', 'user_email', 'article', 'reservation_date', 'status']
