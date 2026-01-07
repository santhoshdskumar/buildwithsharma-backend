from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Service
from .serializers import ServiceSerializer


class NoPagination(PageNumberPagination):
    page_size = None


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True).prefetch_related('features')
    serializer_class = ServiceSerializer
    pagination_class = NoPagination
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        services = Service.objects.filter(is_active=True).prefetch_related('features')
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)
