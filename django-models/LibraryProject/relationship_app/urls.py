from django.urls import path
from .views import views
from.views import LibraryDetailView

urlpatterns = [
    # Function-based view: Shows ALL books
    path('books/', views.list_books, name='book-list'),
    
    # Class-based view: Shows ONE specific library (needs ID)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    # ↑ Added: <int:pk> to tell Django WHICH library
]