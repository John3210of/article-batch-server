from django.urls import path
from .views import HealthCheckView
from .views.article import CategoryListView


urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('category/', CategoryListView.as_view(), name='category-list'),
]

