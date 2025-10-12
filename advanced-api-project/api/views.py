from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters import rest_framework as django_filters
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ------------------------------------------------------------
# BOOK VIEWS - SEPARATED AS REQUIRED
# ------------------------------------------------------------

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    URL: /api/books/
    Method: GET
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # Enable filtering, searching, and ordering
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'id']


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    URL: /api/books/<int:pk>/
    Method: GET
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    URL: /api/books/create/
    Method: POST
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    URL: /api/books/<int:pk>/update/
    Methods: PUT, PATCH
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    URL: /api/books/<int:pk>/delete/
    Method: DELETE
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ------------------------------------------------------------
# AUTHOR VIEWS - SEPARATED AS REQUIRED
# ------------------------------------------------------------

class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors.
    URL: /api/authors/
    Method: GET
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    # Enable search, filter, and ordering
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID.
    URL: /api/authors/<int:pk>/
    Method: GET
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new author.
    URL: /api/authors/create/
    Method: POST
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing author.
    URL: /api/authors/<int:pk>/update/
    Methods: PUT, PATCH
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing an author.
    URL: /api/authors/<int:pk>/delete/
    Method: DELETE
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]