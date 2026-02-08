from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

# == Generic API Views ==
class ListAPIView(generics.ListAPIView):
    """
    Generic API view for listing objects.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]



class ListCreateAPIView(generics.ListCreateAPIView):
    """
    Generic API view for listing and creating objects.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        return super().perform_create(serializer)
    permission_classes = [IsAuthenticated]

    

class DetailAPIView(generics.RetrieveAPIView):
    """
    Generic API view for retrieving a single object.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateAPIView(generics.UpdateAPIView):
    """
    Generic API view for updating an existing object.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def perform_update(self, serializer):
        book = self.get_object()
        user = self.request.user
        if book.owner != user:
            raise PermissionDenied("You do not have permission to edit this book.")
        return super().perform_update(serializer)
    permission_classes = [IsAuthenticated]
    


class DeleteAPIView(generics.DestroyAPIView):
    """
    Generic API view for deleting an existing object.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated]
