from django.urls import path
from . import views

# == URL Patterns to connect API endpoints to views ==
urlpatterns = [
    path('list/', views.ListAPIView.as_view(), name='list'),
    path('list-create/', views.ListCreateAPIView.as_view(), name='list-create'),
    path('detail/<int:pk>/', views.DetailAPIView.as_view(), name='detail'),
    path('update/<int:pk>/', views.UpdateAPIView.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteAPIView.as_view(), name='delete'),

]