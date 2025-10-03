# UPDATE ONLY THESE SPECIFIC TEST METHODS - keep everything else as is

def test_book_list_view(self):
    """GET /api/books/ should list all books using BookListView"""
    url = reverse('book-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Check for paginated results
    if 'results' in response.data:
        self.assertGreaterEqual(len(response.data['results']), 3)
    else:
        self.assertGreaterEqual(len(response.data), 3)

def test_author_list_view(self):
    """GET /api/authors/ should list all authors using AuthorListView"""
    url = reverse('author-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Check for paginated results
    if 'results' in response.data:
        self.assertGreaterEqual(len(response.data['results']), 2)
    else:
        self.assertGreaterEqual(len(response.data), 2)

# UPDATE ALL FILTERING/SEARCHING/ORDERING TESTS TO HANDLE PAGINATION
def test_filter_by_publication_year(self):
    """BookListView: Filtering books by publication_year should return only matching results"""
    url = reverse('book-list') + '?publication_year=1963'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    years = [item['publication_year'] for item in results]
    self.assertTrue(all(y == 1963 for y in years))

def test_filter_by_author(self):
    """BookListView: Filtering books by author should return only matching results"""
    url = reverse('book-list') + f'?author={self.author1.id}'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    authors = [item['author'] for item in results]
    self.assertTrue(all(a == self.author1.id for a in authors))

def test_search_by_title(self):
    """BookListView: Search filter should match partial titles"""
    url = reverse('book-list') + '?search=Gatsby'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    titles = [item['title'] for item in results]
    self.assertTrue(any('Gatsby' in t for t in titles))

def test_ordering_by_publication_year_ascending(self):
    """BookListView: Ordering results by publication_year should return them sorted ascending"""
    url = reverse('book-list') + '?ordering=publication_year'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    pub_years = [item['publication_year'] for item in results]
    self.assertEqual(pub_years, sorted(pub_years))

def test_ordering_by_publication_year_descending(self):
    """BookListView: Ordering results by -publication_year should return them sorted descending"""
    url = reverse('book-list') + '?ordering=-publication_year'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    pub_years = [item['publication_year'] for item in results]
    self.assertEqual(pub_years, sorted(pub_years, reverse=True))

def test_ordering_by_title(self):
    """BookListView: Ordering results by title should return them alphabetically"""
    url = reverse('book-list') + '?ordering=title'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    titles = [item['title'] for item in results]
    self.assertEqual(titles, sorted(titles))

def test_author_search_by_name(self):
    """AuthorListView: Search filter should match author names"""
    url = reverse('author-list') + '?search=Kwame'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    names = [item['name'] for item in results]
    self.assertTrue(any('Kwame' in name for name in names))

def test_author_ordering_by_name(self):
    """AuthorListView: Ordering results by name should return them alphabetically"""
    url = reverse('author-list') + '?ordering=name'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # FIX: Handle paginated response
    results = response.data['results'] if 'results' in response.data else response.data
    names = [item['name'] for item in results]
    self.assertEqual(names, sorted(names))