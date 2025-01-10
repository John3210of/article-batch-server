from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class HealthCheckView(APIView):
    @swagger_auto_schema(
    tags=["Health check API"],
    )
    def get(self, request):
        '''
        Health Check for Article app
        '''
        return Response({"ok ok"})