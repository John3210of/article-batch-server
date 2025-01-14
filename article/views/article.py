from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from article.models.articles.category import Category
from article.models.articles.article import Article
from article.serializers.articles.category_serializers import CategorySerializer
from article.serializers.articles.article_serializers import ArticleSerializer
from article.serializers.base_serializers import BaseResponseSerializer
class CategoryViewSet(viewsets.ViewSet):
    """
    Category 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        tags=["Category API"],
        responses={
            200: BaseResponseSerializer,
            400: BaseResponseSerializer,
            404: BaseResponseSerializer,
        },
    )
    def retrieve(self, request, pk=None):
        """
        특정 Category를 조회합니다.
        """
        if not pk:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "Category ID is required"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=pk)
            serialized_data = CategorySerializer(category).data
            response_data = {
                "data": serialized_data
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Category not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Category API"], responses={200: BaseResponseSerializer})
    def list(self, request):
        """
        모든 Category를 조회합니다.
        """
        categories = Category.objects.all()
        serialized_data = CategorySerializer(categories, many=True).data
        response_data = {
            "data": serialized_data
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={201: BaseResponseSerializer, 400: BaseResponseSerializer},
        tags=["Category API"]
    )
    def create(self, request):
        """
        새로운 Category를 생성합니다.
        """
        serializer = CategorySerializer(data=request.data)
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
        request_body=CategorySerializer,
        responses={200: BaseResponseSerializer, 400: BaseResponseSerializer, 404: BaseResponseSerializer},
        tags=["Category API"]
    )
    def partial_update(self, request, pk=None):
        """
        특정 Category를 부분 업데이트합니다.
        """
        if not request.data:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "Request body is empty"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "data": serializer.data
                }
                return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": serializer.errors
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        except Category.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Category not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

class ArticleViewSet(viewsets.ViewSet):
    """
    Article 관련 ViewSet입니다.
    """
    @swagger_auto_schema(
        tags=["Article API"],
        responses={
            200: BaseResponseSerializer,
            400: BaseResponseSerializer,
            404: BaseResponseSerializer,
        },
    )
    def retrieve(self, request, pk=None):
        """
        특정 Article을 조회합니다.
        """
        if not pk:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "Article ID is required"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = Article.objects.get(pk=pk)
            serialized_data = ArticleSerializer(article).data
            response_data = {
                "data": serialized_data
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

        except Article.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Article not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Article API"], responses={200: BaseResponseSerializer})
    def list(self, request):
        """
        모든 Article을 조회합니다.
        """
        articles = Article.objects.all()
        serialized_data = ArticleSerializer(articles, many=True).data
        response_data = {
            "data": serialized_data
        }
        return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ArticleSerializer,
        responses={201: BaseResponseSerializer, 400: BaseResponseSerializer},
        tags=["Article API"]
    )
    def create(self, request):
        """
        새로운 Article을 생성합니다 (단일 또는 다중).
        """
        is_many = isinstance(request.data, list)
        serializer = ArticleSerializer(data=request.data, many=is_many)

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
        request_body=ArticleSerializer,
        responses={200: BaseResponseSerializer, 400: BaseResponseSerializer, 404: BaseResponseSerializer},
        tags=["Article API"]
    )
    def partial_update(self, request, pk=None):
        """
        특정 Article을 부분 업데이트합니다.
        """
        if not request.data:
            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": {"message": "Request body is empty"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "data": serializer.data
                }
                return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_200_OK)

            response_data = {
                "success": False,
                "errorCode": "ERR400",
                "data": serializer.errors
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_400_BAD_REQUEST)

        except Article.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Article not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={204: "No Content", 404: BaseResponseSerializer},
        tags=["Article API"]
    )
    def destroy(self, request, pk=None):
        """
        특정 Article을 삭제합니다.
        """
        try:
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist:
            response_data = {
                "success": False,
                "errorCode": "ERR404",
                "data": {"message": "Article not found"}
            }
            return Response(BaseResponseSerializer(response_data).data, status=status.HTTP_404_NOT_FOUND)
