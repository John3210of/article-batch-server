from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views.user_info import UserCategoryViewSet
from article.views import HealthCheckView
from article.views.article import CategoryViewSet
router = DefaultRouter()
router.register(r'user-category', UserCategoryViewSet, basename='user-category')
router.register(r'category', CategoryViewSet, basename='category')
urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('', include(router.urls)),
]
