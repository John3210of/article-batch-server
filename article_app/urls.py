from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article_app.views.article_viewsets import ArticleViewSet
from article_app.views.category_viewsets import CategoryViewSet
from article_app.views.user_category_viewsets import UserCategoryViewSet
from article_app.views.user_schedule_viewsets import UserScheduleViewSet
from article_app.views import HealthCheckView
from article_app.views.mail_batch_viewsets import MailBatchListView

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'user-category', UserCategoryViewSet, basename='user-category')
router.register(r'user-schedule', UserScheduleViewSet, basename='user-schedule')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('mail-batches/', MailBatchListView.as_view(), name='mail-batches'),
    path('', include(router.urls)),
]
