from django.urls import path, include
from api.views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet


# == Router for BookViewSet  View == #
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# == Urls for BookSerializer  View == #

urlpatterns = [
    path('books/', BookList.as_view(), name = 'book-list'), # Maps to the BookList View
    path('', include(router.urls)),
] 

