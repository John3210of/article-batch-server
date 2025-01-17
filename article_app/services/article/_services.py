from article_app.models import Article
from article_app.serializers.article_serializers import ArticleSerializer
from article_app.services.utils.service_utils import create_response, exception_handler
from article_app.services.base._service import BaseService

class ArticleService(BaseService):

    @staticmethod
    def get_article_by_id(article_id):
        """
        단일 Article 조회
        """
        return BaseService.get_object_by_id(Article, ArticleSerializer, article_id)

    @staticmethod
    def get_all_articles():
        """
        모든 Articles 조회
        """
        return BaseService.get_all_objects(Article, ArticleSerializer)
    
    @staticmethod
    def create_articles(data_list):
        """
        여러 새 Article 생성
        """
        if not isinstance(data_list, list):
            raise ValueError("Input data must be a list of articles.")
        print("==="*20)
        print(data_list)
        print("==="*20)
        return BaseService.bulk_create_objects(ArticleSerializer, data_list)

    # @staticmethod
    # def create_articles(data):
    #     """
    #     새 Article 생성
    #     """
    #     return BaseService.create_object(ArticleSerializer, data)

    @staticmethod
    def update_article(article_id, data):
        """
        기존 Article 업데이트
        """
        return BaseService.update_object(Article, ArticleSerializer, article_id, data)

    @staticmethod
    @exception_handler(method_name="delete_article")
    def delete_article(article_id):
        """
        특정 Article 삭제
        """
        article = Article.objects.get(pk=article_id)
        article.delete()
        return create_response(data={"message": "Article deleted successfully"}, status_code=204)
