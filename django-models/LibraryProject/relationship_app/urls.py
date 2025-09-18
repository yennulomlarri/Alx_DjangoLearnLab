from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, BookListView, LibraryDetailView, AuthorDetailView, member_view, librarian_view, admin_view, add_book, edit_book, delete_book  # ← ADDED THE 3 NEW VIEWS

urlpatterns = [
    # Authentication URLs (EXISTING CODE)
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
    
    # Role-based URLs (EXISTING CODE)
    path('member/', member_view, name='member_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('admin/', admin_view, name='admin_view'),
    
    # ← NEW PERMISSION-BASED URLs (ADDED THIS SECTION)
    path('add_book/', add_book, name='add_book'),  # ← CHANGE to exact pattern
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),  # ← CHANGE to exact pattern
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),  # ← Keep this or update if needed
    # ← END OF NEW PERMISSION-BASED URLs
    
    # Your existing URLs (EXISTING CODE)
    path('books/', list_books, name='book_list'),
    path('books-class/', BookListView.as_view(), name='book_list_class'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
]