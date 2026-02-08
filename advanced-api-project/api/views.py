from django.shortcuts import render
from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter

# == Generic API Views ==
class ListView(generics.ListAPIView):
    """
    Generic API view for listing objects.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', 'description']
    ordering_fields = ['title', 'publicatiob_year', 'created_at']
    ordering = ['title'] #Default
    permission_classes = [IsAuthenticatedOrReadOnly]



class CreateView(generics.ListCreateAPIView):
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

    

class DetailView(generics.RetrieveAPIView):
    """
    Generic API view for retrieving a single object.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateView(generics.UpdateAPIView):
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
    


class DeleteView(generics.DestroyAPIView):
    """
    Generic API view for deleting an existing object.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated]
