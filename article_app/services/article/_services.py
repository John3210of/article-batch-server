from article_app.models import Article
from article_app.serializers.article_serializers import ArticleSerializer
from article_app.services.utils.service_utils import create_response,handle_unexpected_error

class ArticleService:
    @staticmethod
    def get_article_by_id(article_id):
        try:
            article = Article.objects.get(pk=article_id)
            serialized_data = ArticleSerializer(article).data
            return create_response(data=serialized_data)
        except Article.DoesNotExist:
            return create_response(
                success=False,
                error_code="ERR404",
                data={"message": "Article not found"},
                status_code=404
            )
        except Exception as e:
            return handle_unexpected_error(e, "get_article_by_id")

    @staticmethod
    def get_all_articles():
        try:
            articles = Article.objects.all()
            serialized_data = ArticleSerializer(articles, many=True).data
            return create_response(data=serialized_data)
        except Exception as e:
            return handle_unexpected_error(e, "get_all_articles")

    @staticmethod
    def create_articles(data):
        try:
            serializer = ArticleSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return create_response(data=serializer.data)
            else:
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=serializer.errors,
                    status_code=400
                )
        except Exception as e:
            return handle_unexpected_error(e, "create_articles")

    @staticmethod
    def update_article(article_id, data):
        try:
            article = Article.objects.get(pk=article_id)
            serializer = ArticleSerializer(article, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return create_response(data=serializer.data)
            else:
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=serializer.errors,
                    status_code=400
                )
        except Article.DoesNotExist:
            return create_response(
                success=False,
                error_code="ERR404",
                data={"message": "Article not found"},
                status_code=404
            )
        except Exception as e:
            return handle_unexpected_error(e, "update_article")

    @staticmethod
    def delete_article(article_id):
        try:
            article = Article.objects.get(pk=article_id)
            article.delete()
            return create_response(data={"message": "Article deleted successfully"}, status_code=204)
        except Article.DoesNotExist:
            return create_response(
                success=False,
                error_code="ERR404",
                data={"message": "Article not found"},
                status_code=404
            )
        except Exception as e:
            return handle_unexpected_error(e, "delete_article")
