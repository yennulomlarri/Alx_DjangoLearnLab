from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
]