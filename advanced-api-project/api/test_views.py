from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # create a user (for authenticated operations)
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create authors
        self.author1 = Author.objects.create(name="Kwame Nkrumah")
        self.author2 = Author.objects.create(name="F. Scott Fitzgerald")

        # Create books
        self.book1 = Book.objects.create(title="Ghana: The Autobiography of Kwame Nkrumah", publication_year=1957, author=self.author1)
        self.book2 = Book.objects.create(title="Africa Must Unite", publication_year=1963, author=self.author1)
        self.book3 = Book.objects.create(title="The Great Gatsby", publication_year=1925, author=self.author2)
        self.client = APIClient()

    def test_list_books(self):
        """GET /api/books/ should list all books"""
        url = reverse('book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect at least the three books we created
        self.assertGreaterEqual(len(response.data), 3)

    def test_create_book_requires_authentication(self):
        """Unauthenticated POST should be denied; authenticated POST should succeed"""
        url = reverse('book-list-create')
        payload = {
            "title": "Things Fall Apart",
            "publication_year": 1958,
            "author": self.author1.id
        }

        # Unauthenticated attempt => should be 403 because views require auth for create
        response_unauth = self.client.post(url, payload, format='json')
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate and try again
        self.client.force_authenticate(user=self.user)
        response_auth = self.client.post(url, payload, format='json')
        self.assertEqual(response_auth.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_auth.data['title'], "Things Fall Apart")
        self.client.force_authenticate(user=None)  # logout

    def test_retrieve_book_detail(self):
        """GET /api/books/<id>/ should return the book detail"""
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_update_book(self):
        """Authenticated user can update a book; changes persist"""
        url = reverse('book-detail', kwargs={'pk': self.book2.id})
        update_payload = {
            "title": "Africa Must Unite (Updated)",
            "publication_year": 1963,
            "author": self.author1.id
        }

        # Unauthenticated should be forbidden
        response_unauth = self.client.put(url, update_payload, format='json')
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated update
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Africa Must Unite (Updated)")
        self.client.force_authenticate(user=None)

    def test_delete_book(self):
        """Authenticated user can delete a book; unauthenticated cannot"""
        url = reverse('book-detail', kwargs={'pk': self.book3.id})

        # Unauthenticated delete should be forbidden
        response_unauth = self.client.delete(url)
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated delete should succeed
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        # The book should be removed from DB
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book3.id)
        self.client.force_authenticate(user=None)

    def test_filter_by_publication_year(self):
        """Filtering books by publication_year should return only matching results"""
        url = reverse('book-list-create') + '?publication_year=1963'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # only book2 has year 1963
        years = [item['publication_year'] for item in response.data]
        self.assertTrue(all(y == 1963 for y in years))

    def test_search_by_title(self):
        """Search filter should match partial titles"""
        url = reverse('book-list-create') + '?search=Gatsby'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect at least one result and its title to contain 'Gatsby'
        titles = [item['title'] for item in response.data]
        self.assertTrue(any('Gatsby' in t for t in titles))

    def test_ordering_by_publication_year(self):
        """Ordering results by publication_year should return them sorted"""
        url = reverse('book-list-create') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pub_years = [item['publication_year'] for item in response.data]
        self.assertEqual(pub_years, sorted(pub_years))
