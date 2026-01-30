from django.urls import path
from api.views import BookList

# == Urls for BookSerializer  View == #

url_patterns = [
    path('books/', BookList.as_view(), name = 'book-list') # Maps to the BookList View
] 