from enum import Enum

class MailStatus(Enum):
    CREATED = 'CREATED'
    PENDING = 'PENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'

    @classmethod
    def choices(cls):
        """ENUM 데이터를 Django 모델 필드의 choices로 변환"""
        return [(status.value, status.name.capitalize()) for status in cls]