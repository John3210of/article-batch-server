from article_app.models.user_category._models import UserCategory
from article_app.serializers import UserCategoryCreateSerializer, UserCategorySerializer
from article_app.services.utils.service_utils import create_response, exception_handler
from django.db import transaction
from article_app.services.base._service import BaseService
from typing import Set, Tuple
from django.db.models.query import QuerySet

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
        active_categories = UserCategory.objects.get_active_user_category(user_id)
        category_titles = [active_category.category.title for active_category in active_categories]
        response_data = {
            "userId": user_id,
            "categoryTitles": category_titles
        }
        return create_response(data=response_data)

    @staticmethod
    @exception_handler(method_name="create_or_update_user_categories")
    def create_or_update_user_categories(data: dict) -> dict:
        """
        새로운 UserCategory를 생성하거나 업데이트합니다.
        구독 취소 > 재구독 의 경우 기존 정보를 가지고 메일 발송해야 하므로 soft delete 형태로 구현되어있습니다.
        """
        serializer = UserCategoryCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user_id: int = validated_data["user_id"]
        user_email: str = validated_data["user_email"]
        new_category_ids: Set[int] = set(validated_data["category_ids"])

        existing_user_categories: QuerySet[UserCategory] = UserCategory.objects.get_active_user_category(user_id)
        existing_category_ids: Set[int] = set(existing_user_categories.values_list("category_id", flat=True))

        categories_to_add, categories_to_deactivate, categories_to_reactivate = UserCategoryService._categorize_changes(
            existing_user_categories, new_category_ids, existing_category_ids
        )

        UserCategoryService._apply_category_changes(
            user_email, categories_to_add, categories_to_deactivate, categories_to_reactivate, user_id
        )

        updated_user_categories: QuerySet[UserCategory] = UserCategory.objects.get_active_user_category(user_id)
        response_serializer = UserCategorySerializer(updated_user_categories, many=True)

        return create_response(data=response_serializer.data, status_code=201)

    def _categorize_changes(
        existing_user_categories: QuerySet[UserCategory],
        new_category_ids: Set[int],
        existing_category_ids: Set[int]
    ) -> Tuple[Set[int], Set[int], QuerySet[UserCategory]]:
        """
        카테고리 추가, 비활성화, 재활성화 그룹화
        """
        categories_to_add: Set[int] = new_category_ids - existing_category_ids
        categories_to_deactivate: Set[int] = existing_category_ids - new_category_ids
        categories_to_reactivate: QuerySet[UserCategory] = existing_user_categories.filter(
            category_id__in=categories_to_add, is_activated=False
        )

        categories_to_add -= set(categories_to_reactivate.values_list("category_id", flat=True))

        return categories_to_add, categories_to_deactivate, categories_to_reactivate

    def _apply_category_changes(
        user_email: str,
        categories_to_add: Set[int],
        categories_to_deactivate: Set[int],
        categories_to_reactivate: QuerySet[UserCategory],
        user_id: int
    ) -> None:
        """
        변경 사항을 데이터베이스에 반영 (트랜잭션 적용)
        """
        try:
            with transaction.atomic():
                if categories_to_deactivate:
                    UserCategory.objects.filter(
                        user_id=user_id,
                        category_id__in=categories_to_deactivate
                    ).update(is_activated=False)

                if categories_to_reactivate.exists():
                    categories_to_reactivate.update(is_activated=True)

                if categories_to_add:
                    user_categories_to_create = [
                        UserCategory(
                            user_id=user_id,
                            user_email=user_email,
                            category_id=category_id,
                            is_activated=True
                        )
                        for category_id in categories_to_add
                    ]
                    UserCategory.objects.bulk_create(user_categories_to_create)
        except Exception as e:
            print(f"Error during category changes: {e}")
            raise