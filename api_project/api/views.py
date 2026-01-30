from django.shortcuts import render
from rest_framework import viewsets
from api.models import Book
from .serializers import BookSerializer
from rest_framework import generics

# == BookList View that returns data using the seializer == #

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class  = BookSerializer