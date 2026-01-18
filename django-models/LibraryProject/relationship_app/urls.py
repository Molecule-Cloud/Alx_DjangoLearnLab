from django.urls import path
from . import views
from.views import LibraryDetailView
from .views import list_books
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Function-based view: Shows ALL books
    path('books/', views.list_books, name='book-list'),
    
    # Class-based view: Shows ONE specific library (needs ID)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),

    #AUHTHENTICATION URLS
    path('login/', views.LoginView, name = 'login'),
    path('logout/', views.LogoutView, name = 'logout'),
    path('register/', views.register, name = 'register'),

    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),


    path('admin/dashboard', views.admin_view, name='admin-dashboard'),
    path('librarian/dashboard', views.librarian_view, name='librarian-dashboard'),
    path('member/dashboard', views.member_view, name='member-dashboard'),
]