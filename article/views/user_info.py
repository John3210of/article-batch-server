from rest_framework import viewsets, status
from rest_framework.response import Response
from article.models.user_info.user_category import UserCategory
from article.serializers.user_info.user_info_serializers import UserCategorySerializer, UserCategoryCreateSerializer
from article.serializers.base_serializers import BaseResponseSerializer
from drf_yasg.utils import swagger_auto_schema

class UserCategoryViewSet(viewsets.ModelViewSet):
    #TODO Error handle
    """
    UserCategory 관련 Viewset입니다.
    기본 메서드를 사용하며 user_email을 lookup_field로 설정합니다.
    """
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer
    lookup_field = 'user_email'

    @swagger_auto_schema(tags=["User Category API"])
    def list(self, request, *args, **kwargs):
        """
        모든 UserCategory를 조회합니다.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "data": serializer.data
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["User Category API"])
    def retrieve(self, request, *args, **kwargs):
        """
        특정 UserCategory를 조회합니다.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                "data": serializer.data
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)
        except UserCategory.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "UserCategory not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=UserCategoryCreateSerializer,
        responses={
            201: BaseResponseSerializer,
            400: BaseResponseSerializer
        },
        tags=["User Category API"]
    )
    def create(self, request, *args, **kwargs):
        """
        새로운 UserCategory를 생성합니다.
        """
        serializer = UserCategoryCreateSerializer(data=request.data)
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

    @swagger_auto_schema(
        request_body=UserCategoryCreateSerializer,
        responses={
            200: BaseResponseSerializer,
            400: BaseResponseSerializer,
            404: BaseResponseSerializer
        },
        tags=["User Category API"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        userEmail과 categoryId 리스트를 받아 is_activated 상태를 토글합니다.
        """
        instance = self.get_object()
        user_email = instance.user_email
        category_ids = request.data.get('categoryIds')

        if not category_ids or not isinstance(category_ids, list):
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "categoryIds must be a list"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        updated_categories = []
        not_found_categories = []

        for category_id in category_ids:
            try:
                user_category = UserCategory.objects.get(user_email=user_email, category=category_id)
                user_category.is_activated = not user_category.is_activated
                user_category.save()
                updated_categories.append({
                    "categoryId": category_id,
                    "isActivated": user_category.is_activated
                })
            except UserCategory.DoesNotExist:
                not_found_categories.append(category_id)

        response_data = {
            "success": True,
            "errorCode": None,
            "data": {
                "updatedCategories": updated_categories,
                "notFoundCategories": not_found_categories
            }
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """
        PUT 메서드는 비활성화 합니다.
        """
        response_data = {
            "success": False,
            "errorCode": "ERR405",
            "data": {"message": "Method Not Allowed"}
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE 메서드는 비활성화 합니다.
        """
        response_data = {
            "success": False,
            "errorCode": "ERR405",
            "data": {"message": "Method Not Allowed"}
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
