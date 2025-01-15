import logging
from django.core.management.base import BaseCommand
from article_app.services.mail_batch._service import MailBatchService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mail_create_batch.log"),
        logging.StreamHandler()
    ]
)

class Command(BaseCommand):
    help = "send mail batches for today."

    def handle(self, *args, **kwargs):
        logging.info("Starting mail_send_batch creation...")
        try:
            MailBatchService.create_batches_for_next_day()
            logging.info("Batch creation completed successfully.")
        except Exception as e:
            logging.error(f"Error occurred during batch sending: {e}")
            raise e
