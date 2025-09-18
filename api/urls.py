from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Keep the original endpoint for backward compatibility
    path('books/', BookList.as_view({'get': 'list'}), name='book-list'),
    
    # Include all router URLs for the ViewSet
    path('', include(router.urls)),
]