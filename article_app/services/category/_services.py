from article_app.models import Category
from article_app.serializers.category_serializers import CategorySerializer
from article_app.services.utils.service_utils import create_response,handle_unexpected_error

class CategoryService:
    @staticmethod
    def get_category_by_id(category_id):
        """
        특정 Category 조회
        """
        try:
            category = Category.objects.get(pk=category_id)
            serialized_data = CategorySerializer(category).data
            return create_response(success=True, data=serialized_data, status_code=200)
        except Category.DoesNotExist:
            return create_response(
                success=False,
                error_code="ERR404",
                data={"message": "Category not found"},
                status_code=404
            )
        except Exception as e:
            return handle_unexpected_error(e, "get_category_by_id")

    @staticmethod
    def get_all_categories():
        """
        모든 Category 조회
        """
        try:
            categories = Category.objects.all()
            serialized_data = CategorySerializer(categories, many=True).data
            return create_response(success=True, data=serialized_data, status_code=200)
        except Exception as e:
            return handle_unexpected_error(e, "get_all_categories")

    @staticmethod
    def create_category(data):
        """
        새로운 Category 생성
        """
        try:
            serializer = CategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return create_response(success=True, data=serializer.data, status_code=201)
            else:
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=serializer.errors,
                    status_code=400
                )
        except Exception as e:
            return handle_unexpected_error(e, "create_category")

    @staticmethod
    def update_category(category_id, data):
        """
        특정 Category 업데이트
        """
        try:
            category = Category.objects.get(pk=category_id)
            serializer = CategorySerializer(category, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return create_response(success=True, data=serializer.data, status_code=200)
            else:
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=serializer.errors,
                    status_code=400
                )
        except Category.DoesNotExist:
            return create_response(
                success=False,
                error_code="ERR404",
                data={"message": "Category not found"},
                status_code=404
            )
        except Exception as e:
            return handle_unexpected_error(e, "update_category")
