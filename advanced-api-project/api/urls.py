from django.urls import path
from . import views

urlpatterns = [
    # Book URLs
    path('books/', views.BookListView.as_view(), name='book-list'),  # GET all books
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),  # POST new book
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # GET one book
    path('books/<int:pk>/update/', views.BookDetailView.as_view(), name='book-update'),  # PUT/PATCH update
    path('books/<int:pk>/delete/', views.BookDetailView.as_view(), name='book-delete'),  # DELETE
    
    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
]