from rest_framework import generics
from django_filters import rest_framework as filters
from .models import AccessLog
from .serializers import AccessLogSerializer

class AccessLogFilter(filters.FilterSet):
    card_id = filters.CharFilter(lookup_expr='iexact')
    door_name = filters.CharFilter(lookup_expr='icontains')
    access_granted = filters.BooleanFilter()
    
    class Meta:
        model = AccessLog
        fields = ['card_id', 'door_name', 'access_granted']

class AccessLogListCreateView(generics.ListCreateAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    filterset_class = AccessLogFilter

class AccessLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    
    def perform_update(self, serializer):
        serializer.save()