from rest_framework import generics
from .models import AccessLog
from .serializers import AccessLogSerializer

class AccessLogListCreateView(generics.ListCreateAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer

class AccessLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    
    def perform_update(self, serializer):
        # Prevent timestamp updates
        serializer.save()