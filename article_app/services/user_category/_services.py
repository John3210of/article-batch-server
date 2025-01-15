from article_app.models.user_category._models import UserCategory
from article_app.serializers.user_category_serializers import UserCategoryCreateSerializer, UserCategorySerializer
from article_app.services.utils.service_utils import create_response, handle_unexpected_error

class UserCategoryService:
    @staticmethod
    def list_all_user_categories():
        """
        모든 UserCategory를 조회합니다.
        """
        try:
            queryset = UserCategory.objects.all()
            serializer = UserCategorySerializer(queryset, many=True)
            return create_response(success=True, data=serializer.data, status_code=200)
        except Exception as e:
            return handle_unexpected_error(e, "list_all_user_categories")

    @staticmethod
    def retrieve_user_categories_by_user_id(user_id:int):
        """
        특정 사용자의 활성화된 UserCategory를 조회합니다.
        """
        try:
            categories = UserCategory.objects.filter(user_id=user_id)
            active_categories = categories.filter(is_activated=True)
            category_titles = [category.category.title for category in active_categories]
            response_data = {
                "userId": user_id,
                "categoryTitles": category_titles
            }
            return create_response(success=True, data=response_data, status_code=200)
        except Exception as e:
            return handle_unexpected_error(e, "retrieve_user_categories_by_email")

    @staticmethod
    def create_or_update_user_categories(data):
        """
        새로운 UserCategory를 생성하거나 업데이트합니다.
        """
        try:
            serializer = UserCategoryCreateSerializer(data=data)
            if not serializer.is_valid():
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=serializer.errors,
                    status_code=400
                )
            user_id = serializer.validated_data['user_id']
            user_email = serializer.validated_data['user_email']
            new_category_ids = serializer.validated_data['category_ids']
            existing_user_categories = UserCategory.objects.filter(user_email=user_email)
            existing_category_ids = set(existing_user_categories.values_list('category_id', flat=True))
            categories_to_add = set(new_category_ids) - existing_category_ids

            categories_to_deactivate = existing_category_ids - set(new_category_ids)
            UserCategory.objects.filter(user_email=user_email, category_id__in=categories_to_deactivate).update(is_activated=False)

            for category_id in categories_to_add:
                UserCategory.objects.create(user_id=user_id, user_email=user_email, category_id=category_id, is_activated=True)

            updated_user_categories = UserCategory.objects.filter(user_email=user_email, is_activated=True)
            response_serializer = UserCategorySerializer(updated_user_categories, many=True)
            return create_response(success=True, data=response_serializer.data, status_code=201)
        except Exception as e:
            return handle_unexpected_error(e, "create_or_update_user_categories")
