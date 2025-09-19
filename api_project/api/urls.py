from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, ProfileViewSet, ReaderGroupViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'groups', ReaderGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
