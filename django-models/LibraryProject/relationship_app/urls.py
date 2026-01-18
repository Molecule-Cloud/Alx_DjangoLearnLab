from django.urls import path
from . import views
from.views import LibraryDetailView
from .views import list_books

urlpatterns = [
    # Function-based view: Shows ALL books
    path('books/', views.list_books, name='book-list'),
    
    # Class-based view: Shows ONE specific library (needs ID)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),

    #AUHTHENTICATION URLS
    path('login/', views.list_books, name = 'login'),
    path('logout/', views.LogoutView, name = 'logout'),
    path('register/', views.RegisterView, name = 'register'),
]