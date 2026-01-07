from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutContentViewSet, AboutHighlightViewSet

router = DefaultRouter()
router.register(r'content', AboutContentViewSet)
router.register(r'highlights', AboutHighlightViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

