from django.urls import path
from django.http import HttpResponse
from .views import AccessLogListCreateView, AccessLogDetailView

urlpatterns = [
    path('', lambda r: HttpResponse("Access Control API Running")),
    path('api/logs/', AccessLogListCreateView.as_view(), name='accesslog-list-create'),
    path('api/logs/<int:pk>/', AccessLogDetailView.as_view(), name='accesslog-detail'),
]