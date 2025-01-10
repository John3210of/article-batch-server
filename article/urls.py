from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views.user_info import UserCategoryViewSet
from article.views import HealthCheckView
from article.views.article import CategoryListView

router = DefaultRouter()
router.register(r'user-category', UserCategoryViewSet, basename='user-category')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('', include(router.urls)),
]
