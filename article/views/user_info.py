from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from article.models.user_info.user_category import UserCategory
from article.serializers.user_info.user_info_serializers import UserCategorySerializer, UserCategoryCreateSerializer
from article.serializers.base_serializers import BaseResponseSerializer
from drf_yasg.utils import swagger_auto_schema

class UserCategoryViewSet(viewsets.ViewSet):
    """
    UserCategory 관련 Viewset입니다.
    """
    #TODO : ERROR Handle

    @swagger_auto_schema(tags=["User Category API"], responses={200: BaseResponseSerializer})
    @action(detail=False, methods=['get'], url_path='list/all')
    def list_all(self, request):
        """
        모든 데이터 조회
        """
        queryset = UserCategory.objects.all()
        serializer = UserCategorySerializer(queryset, many=True)
        response_data = {
            "data": serializer.data
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["User Category API"],
        responses={200: BaseResponseSerializer, 400: BaseResponseSerializer, 404: BaseResponseSerializer}
    )
    @action(detail=False, methods=['get'], url_path='(?P<user_email>[^/]+)')
    def get_user_category(self, request, user_email=None):
        """
        userEmail을 URL Path Parameter로 받아 특정 유저 데이터 조회
        """
        if not user_email:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "userEmail is required"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        queryset = UserCategory.objects.filter(user_email=user_email)
        if not queryset.exists():
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "No data found for the given userEmail"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

        serializer = UserCategorySerializer(queryset, many=True)
        response_data = {
            "data": serializer.data
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserCategoryCreateSerializer,
        responses={
            201: BaseResponseSerializer,
            400: BaseResponseSerializer
        },
        tags=["User Category API"]
    )
    def create(self, request):
        """
        userEmail과 categoryId를 받아 새로운 UserCategory 생성
        """
        user_email = request.data.get('userEmail')
        category_id = request.data.get('categoryId')

        if not user_email:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "userEmail is required"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        if not category_id:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "categoryId is required"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "user_email": user_email,
            "category": category_id,
            "is_activated": True,
            "sent_mail_count": 0
        }
        serializer = UserCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "data": serializer.data
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_201_CREATED)

        response_data = {
            "success": False,
            "errorCode": "ERR400",
            "data": serializer.errors
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)
