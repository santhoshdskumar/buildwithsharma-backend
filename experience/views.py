from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Experience
from .serializers import ExperienceSerializer


class NoPagination(PageNumberPagination):
    page_size = None


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.filter(is_active=True).prefetch_related('achievements')
    serializer_class = ExperienceSerializer
    pagination_class = NoPagination
