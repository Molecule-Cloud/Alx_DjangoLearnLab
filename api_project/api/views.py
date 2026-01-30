from django.shortcuts import render
from rest_framework import viewsets
from api.models import Book
from api.serializers import BookSerializer
from rest_framework.generics import ListAPIView

# == BookList View that returns data using the seializer == #

class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



