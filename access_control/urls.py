from django.urls import path
from .views import AccessLogListCreateView, AccessLogDetailView

urlpatterns = [
    path('api/logs/', AccessLogListCreateView.as_view(), name='accesslog-list-create'),
    path('api/logs/<int:pk>/', AccessLogDetailView.as_view(), name='accesslog-detail'),
]