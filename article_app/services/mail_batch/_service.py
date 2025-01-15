from datetime import date, timedelta
import random
from django.db import transaction
from article_app.models import UserCategory, Article, MailBatch, UserSchedule
from article_app.enums.day_of_week import DayOfWeek
from article_app.serializers.mail_batch_serializers import MailBatchSerializer
import requests
from article_app.enums.mail_status import MailStatus
from django.conf import settings
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
        """
        메일 전송 API를 호출합니다.
        API : f'{settings.MAIL_SERVER_URL}/api/v1/mail/batch'
        """
        try:
            response = requests.get(f"{settings.MAIL_SERVER_URL}/api/v1/mail/health")
            if response.status_code != 200 or not response.json().get("success"):
                raise Exception("Mail server health check failed.")
        except Exception as e:
            raise RuntimeError(f"Mail server error: {e}")

        today = (date.today() + timedelta(days=1)).isoformat()  # YYYY-MM-DD 포맷
        mail_batches = MailBatch.objects.filter(reservation_date=today)  # 예약된 모든 메일 가져오기

        for mail_batch in mail_batches:
            body = MailBatchService.test_get_mail_batch_details(mail_batch)
            
            mail_batch.status = MailStatus.PENDING.value
            mail_batch.save()
            try:
                api_response = requests.post(
                    f"{settings.MAIL_SERVER_URL}/api/v1/mail/batch",
                    json=body
                )
                api_response.raise_for_status()
                mail_batch.status = MailStatus.SENT.value
                mail_batch.save()
                print(f"Mail sent for batch: {mail_batch.id}, Response: {api_response.json()}")
            except requests.exceptions.RequestException as e:
                mail_batch.status = MailStatus.FAILED.value
                mail_batch.save()
                print(f"Failed to send mail for batch {mail_batch.id}: {e}")

        return "finished"
    
    @staticmethod
    def check_batches_for_next_day():
        """
        다음날 보낼 메일의 내용을 확인해볼 수 있습니다.
        """
        mails = []
        today = (date.today() + timedelta(days=1)).isoformat()
        mail_batches = MailBatch.objects.filter(reservation_date=today)
        # 메일 서버 상태 확인
        try:
            response = requests.get(f"{settings.MAIL_SERVER_URL}/api/v1/mail/health")
            if response.status_code != 200 or not response.json().get("success"):
                raise Exception("Mail server health check failed.")
        except Exception as e:
            raise RuntimeError(f"Mail server error: {e}")

        for mail_batch in mail_batches:
            mails.append(MailBatchService.get_mail_batch_details(mail_batch))

        print(mails)
        return f"{len(mails)} mails prepared for sending."

    @staticmethod
    def get_mail_batch_details(mail_batch:MailBatch):
        """
        Retrieve details for sending an email.
        """
        return {
            "addressList": [mail_batch.user_email],
            "question": mail_batch.article.title,
            "articleLink": f' server domain + {mail_batch.article.id}'
        }
        
    @staticmethod
    def test_get_mail_batch_details(mail_batch:MailBatch):
        """
        Retrieve details for sending an email.
        """
        return {
            "addressList": ["john3210of@gmail.com"],
            "question": mail_batch.article.title,
            "articleLink": f' server domain + {mail_batch.article.id}'
        }