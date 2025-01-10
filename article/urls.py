from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views.user_info import UserCategoryViewSet,UserScheduleViewSet
from article.views import HealthCheckView
from article.views.article import CategoryViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'user-category', UserCategoryViewSet, basename='user-category')
router.register(r'user-schedule', UserScheduleViewSet, basename='user-schedule')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('user-category/<str:user_email>/', UserCategoryViewSet.as_view({'get': 'retrieve'})),
    path('', include(router.urls)),
]
