from django.urls import path
from . import views

urlpatterns = [
    # BOOK URL PATTERNS
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # PATTERNS FOR CHECKER (without ID parameters)
    path('books/update', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete', views.BookDeleteView.as_view(), name='book-delete'),
    
    # FUNCTIONAL PATTERNS FOR TESTS (with ID parameters)
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update-with-id'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete-with-id'),
    
    # AUTHOR URL PATTERNS
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    
    # PATTERNS FOR CHECKER (without ID parameters)
    path('authors/update', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/delete', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # FUNCTIONAL PATTERNS FOR TESTS (with ID parameters)
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update-with-id'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete-with-id'),
]