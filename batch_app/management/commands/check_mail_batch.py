import logging
from django.core.management.base import BaseCommand
from article_app.services import MailBatchService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mail_check_batch.log"),
        logging.StreamHandler()
    ]
)

class Command(BaseCommand):
    help = "send mail batches for today."

    def handle(self, *args, **kwargs):
        logging.info("Starting to check batches ...")
        try:
            MailBatchService.check_batches_for_next_day()
            logging.info("Batch check completed successfully.")
        except Exception as e:
            logging.error(f"Error occurred during batch checking: {e}")
            raise e
