from datetime import date, timedelta
import random
import logging
from django.db import transaction
from article_app.models import UserCategory, Article, MailBatch, UserSchedule
from article_app.enums.day_of_week import DayOfWeek
from article_app.serializers.mail_batch_serializers import MailBatchSerializer
import requests
from article_app.enums.mail_status import MailStatus
from django.conf import settings
from batch_app.services.discord import send_discord_embed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MailBatchService:
    """
    Service class to handle MailBatch creation tasks.
    #TODO 메일 발송 실패시, 재발송에 관한 비즈니스 로직 정의에 따른 개발이 추가되어야 합니다.
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

        mail_batches = []
        with transaction.atomic():
            for _, categories in user_to_categories.items():
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

                mail_batches.append(MailBatch(
                    user_email=chosen_category.user_email,
                    article=next_article,
                    reservation_date=next_day,
                    status=MailStatus.CREATED.value,
                ))

                chosen_category.last_mailed_article_id = next_article.pk
                chosen_category.save()
            MailBatch.objects.bulk_create(mail_batches)
        send_discord_embed(
            title="📬 내일 보낼 메일 리스트 생성 완료",
            description=f"내일 보낼 메일은 **{len(mail_batches)}건**입니다! 🎉",
            color=0x3498db
        )

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
            logging.error(f"Mail server error: {e}")
            raise RuntimeError(f"Mail server error: {e}")

        today = (date.today()).isoformat()
        mail_batches = MailBatch.objects.filter(reservation_date=today).exclude(status=MailStatus.SENT.value)
        total_batches = len(mail_batches)
        success_count = 0
        failure_count = 0

        send_discord_embed(
            title="🚀 메일 전송 시작",
            description=f"총 **{total_batches}건**의 메일 전송을 시작합니다. 📤",
            color=0x3498db
        )


        for mail_batch in mail_batches:
            body = MailBatchService.get_mail_batch_details(mail_batch)
            
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
                success_count += 1
                logging.info(f"Mail sent for batch: {mail_batch.id}, Response: {api_response.json()}")
            except requests.exceptions.RequestException as e:
                mail_batch.status = MailStatus.FAILED.value
                mail_batch.save()
                failure_count += 1
                logging.error(f"Failed to send mail for batch {mail_batch.id}: {e}")
        logging.info("Mail batch sending finished.")
        send_discord_embed(
            title="📧 메일 전송 완료",
            fields=[
                {"name": "성공한 메일", "value": f"**{success_count}건** ✅", "inline": True},
                {"name": "실패한 메일", "value": f"**{failure_count}건** ❌", "inline": True},
            ],
            color=0x2ecc71 if failure_count == 0 else 0xe74c3c
        )
        logging.info(f"{len(mail_batches)} Mail batch sending finished.")
    
    @staticmethod
    def check_batches_for_next_day():
        """
        다음날 보낼 메일의 내용을 확인해볼 수 있습니다.
        """
        mails = []
        today = (date.today() + timedelta(days=1)).isoformat()
        mail_batches = MailBatch.objects.filter(reservation_date=today,status='CREATED')
        
        try:
            response = requests.get(f"{settings.MAIL_SERVER_URL}/api/v1/mail/health")
            if response.status_code != 200 or not response.json().get("success"):
                raise Exception("Mail server health check failed.")
        except Exception as e:
            logging.error(f"Mail server error: {e}")
            raise RuntimeError(f"Mail server error: {e}")

        for mail_batch in mail_batches:
            mails.append(MailBatchService.get_mail_batch_details(mail_batch))

        logging.info(f"{len(mails)} mails prepared for sending.")
        return f"{len(mails)} mails prepared for sending."

    @staticmethod
    def get_mail_batch_details(mail_batch:MailBatch):
        """
        Retrieve details for sending an email.
        """
        return {
            "addressList": [mail_batch.user_email],
            "question": mail_batch.article.title,
            "articleLink": f'{settings.NINEDOCS_SERVER_URL}/{mail_batch.article.id}'
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
