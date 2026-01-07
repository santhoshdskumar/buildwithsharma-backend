from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Technology
from .serializers import TechnologySerializer


class NoPagination(PageNumberPagination):
    page_size = None


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.filter(is_active=True)
    serializer_class = TechnologySerializer
    pagination_class = NoPagination
