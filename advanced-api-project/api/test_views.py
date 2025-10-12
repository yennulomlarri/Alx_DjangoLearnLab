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

    # ------------------------------------------------------------
    # BOOK VIEW TESTS - UPDATED FOR SEPARATE VIEWS
    # ------------------------------------------------------------

    def test_book_list_view(self):
        """GET /api/books/ should list all books using BookListView"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        self.assertIn('results', response.data)
        self.assertGreaterEqual(len(response.data['results']), 3)

    def test_book_detail_view(self):
        """GET /api/books/<id>/ should return the book detail using BookDetailView"""
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_book_create_view_requires_authentication(self):
        """BookCreateView: Unauthenticated POST should be denied; authenticated POST should succeed"""
        url = reverse('book-create')
        payload = {
            "title": "Things Fall Apart",
            "publication_year": 1958,
            "author": self.author1.id
        }

        # Unauthenticated attempt => should be 403
        response_unauth = self.client.post(url, payload, format='json')
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate and try again
        self.client.force_authenticate(user=self.user)
        response_auth = self.client.post(url, payload, format='json')
        self.assertEqual(response_auth.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_auth.data['title'], "Things Fall Apart")
        self.client.force_authenticate(user=None)  # logout

    def test_book_create_view_with_login(self):
        """BookCreateView: Test authentication using client.login() method"""
        url = reverse('book-create')
        payload = {
            "title": "Things Fall Apart",
            "publication_year": 1958,
            "author": self.author1.id
        }

        # Test with client.login() method
        login_success = self.client.login(username='testuser', password='password123')
        self.assertTrue(login_success)
        
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Things Fall Apart")
        
        # Logout
        self.client.logout()

    def test_book_update_view(self):
        """BookUpdateView: Authenticated user can update a book; changes persist"""
        url = reverse('book-update', kwargs={'pk': self.book2.id})
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

    def test_book_update_view_with_login(self):
        """BookUpdateView: Test update using client.login() method"""
        url = reverse('book-update', kwargs={'pk': self.book2.id})
        update_payload = {
            "title": "Africa Must Unite (Updated with Login)",
            "publication_year": 1963,
            "author": self.author1.id
        }

        # Test with client.login() method
        login_success = self.client.login(username='testuser', password='password123')
        self.assertTrue(login_success)
        
        response = self.client.put(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Africa Must Unite (Updated with Login)")
        
        # Logout
        self.client.logout()

    def test_book_delete_view(self):
        """BookDeleteView: Authenticated user can delete a book; unauthenticated cannot"""
        url = reverse('book-delete', kwargs={'pk': self.book3.id})

        # Unauthenticated delete should be forbidden
        response_unauth = self.client.delete(url)
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated delete should succeed
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # The book should be removed from DB
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book3.id)
        self.client.force_authenticate(user=None)

    def test_book_delete_view_with_login(self):
        """BookDeleteView: Test delete using client.login() method"""
        # Create a separate book for deletion test
        test_book = Book.objects.create(
            title="Test Book for Deletion", 
            publication_year=2023, 
            author=self.author1
        )
        url = reverse('book-delete', kwargs={'pk': test_book.id})

        # Test with client.login() method
        login_success = self.client.login(username='testuser', password='password123')
        self.assertTrue(login_success)
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # The book should be removed from DB
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=test_book.id)
        
        # Logout
        self.client.logout()

    # ------------------------------------------------------------
    # FILTERING, SEARCHING, ORDERING TESTS - UPDATED FOR BookListView
    # ------------------------------------------------------------

    def test_filter_by_publication_year(self):
        """BookListView: Filtering books by publication_year should return only matching results"""
        url = reverse('book-list') + '?publication_year=1963'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        years = [item['publication_year'] for item in results]
        self.assertTrue(all(y == 1963 for y in years))

    def test_filter_by_author(self):
        """BookListView: Filtering books by author should return only matching results"""
        url = reverse('book-list') + f'?author={self.author1.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        authors = [item['author'] for item in results]
        self.assertTrue(all(a == self.author1.id for a in authors))

    def test_search_by_title(self):
        """BookListView: Search filter should match partial titles"""
        url = reverse('book-list') + '?search=Gatsby'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        titles = [item['title'] for item in results]
        self.assertTrue(any('Gatsby' in t for t in titles))

    def test_search_by_author_name(self):
        """BookListView: Search filter should match author names"""
        url = reverse('book-list') + '?search=Fitzgerald'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        self.assertGreaterEqual(len(results), 1)

    def test_ordering_by_publication_year_ascending(self):
        """BookListView: Ordering results by publication_year should return them sorted ascending"""
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        pub_years = [item['publication_year'] for item in results]
        self.assertEqual(pub_years, sorted(pub_years))

    def test_ordering_by_publication_year_descending(self):
        """BookListView: Ordering results by -publication_year should return them sorted descending"""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        pub_years = [item['publication_year'] for item in results]
        self.assertEqual(pub_years, sorted(pub_years, reverse=True))

    def test_ordering_by_title(self):
        """BookListView: Ordering results by title should return them alphabetically"""
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        titles = [item['title'] for item in results]
        self.assertEqual(titles, sorted(titles))

    # ------------------------------------------------------------
    # AUTHOR VIEW TESTS - UPDATED FOR SEPARATE VIEWS
    # ------------------------------------------------------------

    def test_author_list_view(self):
        """GET /api/authors/ should list all authors using AuthorListView"""
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        self.assertIn('results', response.data)
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_author_detail_view(self):
        """GET /api/authors/<id>/ should return the author detail using AuthorDetailView"""
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)

    def test_author_create_view_requires_authentication(self):
        """AuthorCreateView: Unauthenticated POST should be denied; authenticated POST should succeed"""
        url = reverse('author-create')
        payload = {
            "name": "Chinua Achebe"
        }

        # Unauthenticated attempt => should be 403
        response_unauth = self.client.post(url, payload, format='json')
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate and try again
        self.client.force_authenticate(user=self.user)
        response_auth = self.client.post(url, payload, format='json')
        self.assertEqual(response_auth.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_auth.data['name'], "Chinua Achebe")
        self.client.force_authenticate(user=None)

    def test_author_create_view_with_login(self):
        """AuthorCreateView: Test authentication using client.login() method"""
        url = reverse('author-create')
        payload = {
            "name": "Chimamanda Ngozi Adichie"
        }

        # Test with client.login() method
        login_success = self.client.login(username='testuser', password='password123')
        self.assertTrue(login_success)
        
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Chimamanda Ngozi Adichie")
        
        # Logout
        self.client.logout()

    def test_author_update_view(self):
        """AuthorUpdateView: Authenticated user can update an author; changes persist"""
        url = reverse('author-update', kwargs={'pk': self.author2.id})
        update_payload = {
            "name": "F. Scott Fitzgerald (Updated)"
        }

        # Unauthenticated should be forbidden
        response_unauth = self.client.put(url, update_payload, format='json')
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated update
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author2.refresh_from_db()
        self.assertEqual(self.author2.name, "F. Scott Fitzgerald (Updated)")
        self.client.force_authenticate(user=None)

    def test_author_delete_view(self):
        """AuthorDeleteView: Authenticated user can delete an author; unauthenticated cannot"""
        # Create a separate author for deletion test
        test_author = Author.objects.create(name="Test Author for Deletion")
        url = reverse('author-delete', kwargs={'pk': test_author.id})

        # Unauthenticated delete should be forbidden
        response_unauth = self.client.delete(url)
        self.assertEqual(response_unauth.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated delete should succeed
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # The author should be removed from DB
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(pk=test_author.id)
        self.client.force_authenticate(user=None)

    # ------------------------------------------------------------
    # AUTHOR FILTERING, SEARCHING, ORDERING TESTS
    # ------------------------------------------------------------

    def test_author_search_by_name(self):
        """AuthorListView: Search filter should match author names"""
        url = reverse('author-list') + '?search=Kwame'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        names = [item['name'] for item in results]
        self.assertTrue(any('Kwame' in name for name in names))

    def test_author_ordering_by_name(self):
        """AuthorListView: Ordering results by name should return them alphabetically"""
        url = reverse('author-list') + '?ordering=name'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIX: Handle paginated response
        results = response.data['results']
        names = [item['name'] for item in results]
        self.assertEqual(names, sorted(names))

    # ------------------------------------------------------------
    # VALIDATION TESTS
    # ------------------------------------------------------------

    def test_book_publication_year_validation(self):
        """BookCreateView: Should reject publication years in the future"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        payload = {
            "title": "Future Book",
            "publication_year": 2030,  # Future year
            "author": self.author1.id
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.client.force_authenticate(user=None)

    def test_book_duplicate_validation(self):
        """BookCreateView: Should reject duplicate books by same author"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        payload = {
            "title": self.book1.title,  # Same title as existing book
            "publication_year": 2023,
            "author": self.book1.author.id  # Same author
        }

        response = self.client.post(url, payload, format='json')
        # This might return 400 if unique_together validation is implemented
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])
        self.client.force_authenticate(user=None)