from article_app.models import Category
from article_app.serializers import CategorySerializer
from article_app.services.base._service import BaseService
class CategoryService(BaseService):

    @staticmethod
    def get_category_by_id(category_id):
        """
        특정 Category 조회
        """
        return BaseService.get_object_by_id(Category, CategorySerializer, category_id)

    @staticmethod
    def get_all_categories():
        """
        모든 Category 조회
        """
        return BaseService.get_all_objects(Category, CategorySerializer)

    @staticmethod
    def create_category(data):
        """
        새로운 Category 생성
        """
        return BaseService.create_object(CategorySerializer, data)

    @staticmethod
    def update_category(category_id, data):
        """
        특정 Category 업데이트
        """
        return BaseService.update_object(Category, CategorySerializer, category_id, data)
