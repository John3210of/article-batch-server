from article_app.models.user_category._models import UserCategory
from article_app.serializers import UserCategoryCreateSerializer, UserCategorySerializer
from article_app.services.utils.service_utils import create_response, exception_handler
from article_app.services.base._service import BaseService
class UserCategoryService(BaseService):
    
    @staticmethod
    def list_all_user_categories():
        """
        모든 UserCategory를 조회합니다.
        """
        return BaseService.get_all_objects(UserCategory, UserCategorySerializer)

    @staticmethod
    @exception_handler(method_name="retrieve_user_categories_by_user_id")
    def retrieve_user_categories_by_user_id(user_id:int):
        """
        특정 사용자의 활성화된 UserCategory를 조회합니다.
        """
        active_categories = UserCategory.objects.filter(user_id=user_id, is_activated=True)
        category_titles = [active_category.category.title for active_category in active_categories]
        response_data = {
            "userId": user_id,
            "categoryTitles": category_titles
        }
        return create_response(data=response_data)

    @staticmethod
    @exception_handler(method_name="create_or_update_user_categories")
    def create_or_update_user_categories(data):
        """
        새로운 UserCategory를 생성하거나 업데이트합니다.
        구독 취소 > 재구독 의 경우 기존 정보를 가지고 메일 발송해야하므로 soft delete 형태로 구현되어있습니다.
        """
        serializer = UserCategoryCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user_id = validated_data['user_id']
        user_email = validated_data['user_email']
        new_category_ids = set(validated_data['category_ids'])
        existing_user_categories = UserCategory.objects.filter(user_email=user_email)
        existing_category_ids = set(existing_user_categories.values_list('category_id', flat=True))

        categories_to_add = new_category_ids - existing_category_ids
        categories_to_deactivate = existing_category_ids - new_category_ids

        categories_to_reactivate = existing_user_categories.filter(category_id__in=categories_to_add, is_activated=False)
        categories_to_add -= set(categories_to_reactivate.values_list('category_id', flat=True))
        UserCategory.objects.filter(user_email=user_email,category_id__in=categories_to_deactivate).update(is_activated=False)
        categories_to_reactivate.update(is_activated=True)

        if categories_to_add:
            user_categories_to_create = [UserCategory(user_id=user_id, user_email=user_email, category_id=category_id, is_activated=True)
            for category_id in categories_to_add
        ]
            UserCategory.objects.bulk_create(user_categories_to_create)
        updated_user_categories = UserCategory.objects.filter(user_email=user_email, is_activated=True)
        response_serializer = UserCategorySerializer(updated_user_categories, many=True)

        return create_response(data=response_serializer.data, status_code=201)