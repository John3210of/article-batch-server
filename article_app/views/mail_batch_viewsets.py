from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from article_app.services.mail_batch._service import MailBatchService

class MailBatchListView(APIView):
    """
    API View to retrieve all MailBatch records.
    """

    @swagger_auto_schema(
        tags=["Mail Batch API"],
        operation_summary="Get all Mail Batches",
        responses={200: "List of all Mail Batches"}
    )
    def get(self, request):
        """
        Retrieve all MailBatch records
        """
        try:
            mail_batches = MailBatchService.get_all_mail_batches()
            return Response(mail_batches, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
