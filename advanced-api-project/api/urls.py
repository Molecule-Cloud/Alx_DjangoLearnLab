from django.urls import path
from . import views


urlpatterns = [
    # RESTful book endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),  # GET list, POST create
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # GET, PUT, PATCH, DELETE
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
]