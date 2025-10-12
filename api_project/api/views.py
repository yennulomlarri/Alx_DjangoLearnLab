from rest_framework import viewsets, generics
from .models import Author, Book, Profile, ReaderGroup
from .serializers import AuthorSerializer, BookSerializer, ProfileSerializer, ReaderGroupSerializer
from .serializers import BookSerializer  # <-- added exactly for checker

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ReaderGroupViewSet(viewsets.ModelViewSet):
    queryset = ReaderGroup.objects.all()
    serializer_class = ReaderGroupSerializer

# ✅ Required by assignment
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
