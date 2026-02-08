# api/test_views.py
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Author

class BookViewTests(APITestCase):
    def setUp(self):
        """Setup test data"""
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='regularpass123'
        )
        
        # Create test data
        self.author = Author.objects.create(name="J.K. Rowling")
        
        self.book1 = Book.objects.create(
            title="Harry Potter and the Sorcerer's Stone",
            publication_year=1997,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author
        )
    
    def test_book_list_view(self):
        """Test GET /api/books/ returns all books"""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_book_authenticated(self):
        """Test authenticated user can create a book using login()"""
        # Login the user
        self.client.login(username='admin', password='adminpass123')
        
        url = reverse('book-list')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """Test unauthenticated user cannot create a book"""
        # Don't login - stay unauthenticated
        
        url = reverse('book-list')
        data = {
            'title': 'Should Fail Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated(self):
        """Test authenticated user can update a book"""
        # Login
        self.client.login(username='admin', password='adminpass123')
        
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author.id
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_book_authenticated(self):
        """Test authenticated user can delete a book"""
        # Login
        self.client.login(username='admin', password='adminpass123')
        
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_filter_by_title(self):
        """Test filtering books by title"""
        url = reverse('book-list') + '?title=Chamber'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_functionality(self):
        """Test search across fields"""
        url = reverse('book-list') + '?search=Chamber'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_ordering_by_year_descending(self):
        """Test ordering books by publication year"""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.book2.title)
    
    def test_logout_functionality(self):
        """Test logout prevents access"""
        # Login first
        self.client.login(username='admin', password='adminpass123')
        
        # Logout
        self.client.logout()
        
        # Try to create book after logout
        url = reverse('book-list')
        data = {'title': 'Should Fail', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)