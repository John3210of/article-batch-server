import logging
from django.core.management.base import BaseCommand
from article_app.services import MailBatchService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mail_send_batch.log"),
        logging.StreamHandler()
    ]
)

class Command(BaseCommand):
    help = "Create mail batches for the next day."

    def handle(self, *args, **kwargs):
        logging.info("Starting batch creation...")
        try:
            MailBatchService.send_batches_for_next_day()
            logging.info("Batch creation completed successfully.")
        except Exception as e:
            logging.error(f"Error occurred during batch creation: {e}")
            raise e
