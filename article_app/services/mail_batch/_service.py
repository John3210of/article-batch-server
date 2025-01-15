from datetime import date, timedelta
import random
from django.db import transaction
from article_app.models import UserCategory, Article, MailBatch, UserSchedule
from article_app.enums.day_of_week import DayOfWeek
from article_app.serializers.mail_batch_serializers import MailBatchSerializer
from asgiref.sync import sync_to_async
class MailBatchService:
    """
    Service class to handle MailBatch creation tasks.
    """

    @staticmethod
    def get_all_mail_batches():
        """
        Retrieve all MailBatch data.
        """
        mail_batches = MailBatch.objects.all()
        return MailBatchSerializer(mail_batches, many=True).data
    
    @staticmethod
    def create_batches_for_next_day():
        """
        Create Mail Batches for the next day's user schedules.
        """
        today = date.today()
        next_day = today + timedelta(days=1)
        next_day_of_week = DayOfWeek(next_day.strftime('%a').upper())

        scheduled_users = UserSchedule.objects.filter(day_of_week=next_day_of_week.value)
        user_ids = [schedule.user_id for schedule in scheduled_users]

        user_categories = UserCategory.objects.filter(is_activated=True, user_id__in=user_ids)

        user_to_categories = {}
        for user_category in user_categories:
            if user_category.user_id not in user_to_categories:
                user_to_categories[user_category.user_id] = []
            user_to_categories[user_category.user_id].append(user_category)
            
        with transaction.atomic():
            for user_id, categories in user_to_categories.items():
                chosen_category = random.choice(categories)
                category = chosen_category.category

                next_article = Article.objects.filter(
                    category=category,
                    pk__gt=chosen_category.last_mailed_article_id
                ).order_by('pk').first()

                if not next_article:
                    #NOTE 다음 Article이 없으면 last_mailed_article_id를 0으로 초기화 합니다.
                    chosen_category.last_mailed_article_id = 0
                    chosen_category.save()
                    continue

                MailBatch.objects.create(
                    user_email=chosen_category.user_email,
                    article=next_article,
                    reservation_date=next_day,
                    status="CREATED",
                )

                chosen_category.last_mailed_article_id = next_article.pk
                chosen_category.save()
                
    @staticmethod
    def send_batches_for_next_day():
        pass
    
    @staticmethod
    def check_batches_for_next_day():
        '''
        다음날 보낼 메일의 내용을 확인해볼 수 있습니다.
        '''
        pass