from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import ContactInfo, ContactSubmission
from .serializers import ContactInfoSerializer, ContactSubmissionSerializer


class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactInfo.objects.filter(is_active=True)
    serializer_class = ContactInfoSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        contact_info = ContactInfo.objects.filter(is_active=True).first()
        if contact_info:
            serializer = self.get_serializer(contact_info)
            return Response(serializer.data)
        return Response(None)


class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    http_method_names = ['post']  # Only allow POST for submissions
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Thank you! Your message has been sent successfully. I\'ll get back to you within 24 hours.'},
            status=status.HTTP_201_CREATED
        )
