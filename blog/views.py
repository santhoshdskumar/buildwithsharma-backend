from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostListSerializer


class NoPagination(PageNumberPagination):
    page_size = None


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    pagination_class = NoPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_post = BlogPost.objects.filter(is_published=True, featured=True).first()
        if featured_post:
            serializer = BlogPostSerializer(featured_post)
            return Response(serializer.data)
        return Response(None)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_posts = BlogPost.objects.filter(is_published=True, featured=False)[:5]
        serializer = BlogPostListSerializer(recent_posts, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Override retrieve to support slug-based lookup
        """
        # Try to get by ID first
        try:
            post = self.get_object()
        except:
            # If ID lookup fails, try slug
            post = BlogPost.objects.filter(slug=pk, is_published=True).first()
            if not post:
                from rest_framework.exceptions import NotFound
                raise NotFound("Blog post not found")
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)