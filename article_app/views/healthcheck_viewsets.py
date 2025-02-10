from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connections
from django.db.utils import OperationalError
from drf_yasg.utils import swagger_auto_schema

class HealthCheckView(APIView):
    @swagger_auto_schema(
        tags=["Health check API"],
    )
    def get(self, request):
        '''
        Health Check for Article app (DB Connection Included)
        '''
        db_status = "ok"
        try:
            db_conn = connections["default"]
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        except OperationalError:
            db_status = "failed"

        return Response({
            "status": "ok",
            "database": db_status
        })
