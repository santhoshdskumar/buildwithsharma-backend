from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import AboutContent, AboutHighlight
from .serializers import AboutContentSerializer, AboutHighlightSerializer


class NoPagination(PageNumberPagination):
    page_size = None


class AboutContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutContent.objects.filter(is_active=True)
    serializer_class = AboutContentSerializer
    pagination_class = NoPagination


class AboutHighlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutHighlight.objects.filter(is_active=True)
    serializer_class = AboutHighlightSerializer
    pagination_class = NoPagination
