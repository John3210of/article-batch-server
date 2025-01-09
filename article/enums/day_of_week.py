from enum import Enum


class DayOfWeek(Enum):
    MON = 'MON'
    TUE = 'TUE'
    WED = 'WED'
    THU = 'THU'
    FRI = 'FRI'
    SAT = 'SAT'
    SUN = 'SUN'

    @classmethod
    def choices(cls):
        """ENUM 데이터를 Django 모델 필드의 choices로 변환"""
        return [(tag.value, tag.name.capitalize()) for tag in cls]
