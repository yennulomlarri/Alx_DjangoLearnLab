from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ------------------------------------------------------------
# AUTHOR VIEWS
# ------------------------------------------------------------
class AuthorListCreateView(generics.ListCreateAPIView):
    """
    GET: List all authors
    POST: Create a new author
    Supports: Search, Filter, Ordering
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # Only authenticated users can create/update/delete, others can read
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Enable search, filter, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']  # allows ?name=Kwame
    search_fields = ['name']     # allows ?search=Kwame
    ordering_fields = ['id', 'name']  # allows ?ordering=name


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve an author by ID
    PUT/PATCH: Update author
    DELETE: Delete author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ------------------------------------------------------------
# BOOK VIEWS
# ------------------------------------------------------------
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: List all books
    POST: Create a new book
    Supports: Filtering, Search, and Ordering
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author']  # e.g., ?publication_year=1960
    search_fields = ['title', 'author__name']          # e.g., ?search=Gatsby
    ordering_fields = ['title', 'publication_year', 'id']  # e.g., ?ordering=title


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a book
    PUT/PATCH: Update a book
    DELETE: Delete a book
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
