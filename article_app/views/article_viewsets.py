from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from article_app.services import ArticleService
from drf_yasg import openapi
from rest_framework.decorators import action
class ArticleViewSet(viewsets.ViewSet):
    """
    Article 관련 ViewSet입니다.
    """
    
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
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "title": openapi.Schema(type=openapi.TYPE_STRING, description="Article title"),
                    "contents": openapi.Schema(type=openapi.TYPE_STRING, description="Article contents"),
                    "link": openapi.Schema(type=openapi.TYPE_STRING, description="Article link"),
                    "categoryTitle": openapi.Schema(type=openapi.TYPE_STRING, description="Category title"),
                },
                required=["title", "contents", "link", "categoryTitle"],
            ),
        ),
        tags=["Article API"]
    )
    def create(self, request):
        '''
        여러 article을 생성하는 API입니다.
        '''
        return ArticleService.create_articles(request.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Article title"),
                "contents": openapi.Schema(type=openapi.TYPE_STRING, description="Article contents"),
                "link": openapi.Schema(type=openapi.TYPE_STRING, description="Article link"),
                "categoryId": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category Id")
            },
            required=["title", "contents", "link", "categoryId"],
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
    
    @swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "articleIds": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER),
                description="조회할 Article ID 목록"
            )
        },
        required=["articleIds"],
    ),
    responses={200: "Success", 400: "Bad Request"},
    tags=["Article API"]
    )
    @action(detail=False, methods=["post"], url_path="retrieve-multiple")
    def retrieve_multiple(self, request):
        '''
        특정 article을 조회하는 API입니다.
        POST 요청에서 `article_ids` 리스트를 받아 해당 article을 반환합니다.
        '''
        article_ids = request.data.get("article_ids")
        return ArticleService.get_articles_by_ids(article_ids)