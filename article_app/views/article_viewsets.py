from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from article_app.services.article._services import ArticleService
from drf_yasg import openapi

class ArticleViewSet(viewsets.ViewSet):
    """
    Article 관련 ViewSet입니다.
    """
    #TODO swagger 일괄 처리
    
    @swagger_auto_schema(
        tags=["Article API"]
    )
    def retrieve(self, request, pk=None):
        '''
        article을 조회하는 API입니다.          
        '''
        return ArticleService.get_article_by_id(pk)

    @swagger_auto_schema(tags=["Article API"])
    def list(self, request):
        '''
        모든 article을 조회하는 API입니다.
        '''
        return ArticleService.get_all_articles()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Article title"),
                "contents": openapi.Schema(type=openapi.TYPE_STRING, description="Article contents"),
                "link": openapi.Schema(type=openapi.TYPE_STRING, description="Article link"),
                "categoryTitle": openapi.Schema(type=openapi.TYPE_STRING, description="Category title")
            },
            required=["title", "contents", "link", "categoryTitle"],
        ),
        tags=["Article API"]
    )
    def create(self, request):
        return ArticleService.create_articles(request.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Article title"),
                "contents": openapi.Schema(type=openapi.TYPE_STRING, description="Article contents"),
                "link": openapi.Schema(type=openapi.TYPE_STRING, description="Article link"),
                "categoryTitle": openapi.Schema(type=openapi.TYPE_STRING, description="Category title")
            },
            required=["title", "contents", "link", "categoryTitle"],
        ),
        tags=["Article API"]
    )
    def partial_update(self, request, pk=None):
        return ArticleService.update_article(pk, request.data)

    @swagger_auto_schema(
        responses={204: "No Content"},
        tags=["Article API"]
    )
    def destroy(self, request, pk=None):
        return ArticleService.delete_article(pk)
