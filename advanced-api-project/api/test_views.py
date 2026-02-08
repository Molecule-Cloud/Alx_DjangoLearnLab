from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Book, Author
import json

class BookAPITests(TestCase):
    def setUp(self):
        """
        Setup test data before each test
        """
        self.admin_user = User.objects.create_user(
            username='admin', password='passwordforadmin123', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular', password='randompassword123'
        )

        self.admin_token = Token.objects.create(
            user=self.admin_user
        )
        self.regular_token = Token.objects.create(
            user=self.regular_user
        )

        # == Test Data == #
        self.author = Author.objects.create(name='Benjamin')
        self.book1 = Book.objects.create(
            title = 'Harward towards success',
            publication_year = 2025,
            author = self.author
        )
        self.book2 = Book.objects.create(
            title = 'The ALX Goal',
            publication_year = 2026,
            author=self.author
        )
        self.client = APIClient()


        def test_get_all_books(self):
            url = reverse('book-list')
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response.data[0]['title'], self.book.title)

        def test_create_book_authenticated(self):
            url = reverse('book-list')
            data = {
                'title': 'The ALX Dream',
                'publication_year': 2025,
                'author': self.author.id
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_update_book(self):
            """Test updating a book"""
            url = reverse('book-detail', args=[self.book1.id])
            data = {
                'title': 'Updated Title',
                'publication_year': 1997,
                'author': self.author.id
            }
            
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
            response = self.client.put(url, data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Refresh from database
            self.book1.refresh_from_db()
            self.assertEqual(self.book1.title, 'Updated Title')
    
        def test_delete_book(self):
            """Test deleting a book"""
            url = reverse('book-detail', args=[self.book1.id])
            
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
            response = self.client.delete(url)
            
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Book.objects.count(), 1)
        
        def test_get_single_book(self):
            """Test retrieving a single book"""
            url = reverse('book-detail', args=[self.book1.id])
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], self.book1.title)
        
        # ===== FILTERING TESTS =====
        
        def test_filter_by_title(self):
            """Test filtering books by title"""
            url = reverse('book-list') + '?title=Chamber'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], self.book2.title)
        
        def test_filter_by_author_name(self):
            """Test filtering books by author name"""
            url = reverse('book-list') + '?author__name=Rowling'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)
        
        def test_filter_by_publication_year(self):
            """Test filtering books by publication year"""
            url = reverse('book-list') + '?publication_year=1997'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], self.book1.title)
        
        def test_filter_by_year_range(self):
            """Test filtering books by year range"""
            url = reverse('book-list') + '?publication_year__gte=1998'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], self.book2.title)
        
        # ===== SEARCHING TESTS =====
        
        def test_search_functionality(self):
            """Test search across fields"""
            url = reverse('book-list') + '?search=Chamber'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
        
        # ===== ORDERING TESTS =====
        
        def test_ordering_by_year_descending(self):
            """Test ordering books by publication year descending"""
            url = reverse('book-list') + '?ordering=-publication_year'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data[0]['title'], self.book2.title)  # 1998
            self.assertEqual(response.data[1]['title'], self.book1.title)  # 1997
        
        def test_ordering_by_title(self):
            """Test ordering books by title"""
            url = reverse('book-list') + '?ordering=title'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # Chamber comes before Sorcerer's alphabetically
            self.assertEqual(response.data[0]['title'], self.book2.title)
        
        # ===== VALIDATION TESTS =====
        
        def test_validation_future_year(self):
            """Test validation rejects future publication year"""
            url = reverse('book-list')
            data = {
                'title': 'Future Book',
                'publication_year': 2050,  # Future year
                'author': self.author.id
            }
            
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
            response = self.client.post(url, data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('publication_year', response.data)
        
        def test_validation_missing_title(self):
            """Test validation requires title"""
            url = reverse('book-list')
            data = {
                'publication_year': 2023,
                'author': self.author.id
            }
            
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
            response = self.client.post(url, data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('title', response.data)
        
        # ===== PERMISSION TESTS =====
        
        def test_admin_vs_regular_user_permissions(self):
            """Test admin vs regular user permissions (if different)"""
            # Add a book with owner field if your model has it
            pass  # Modify based on your actual permission setup
        
        # ===== NESTED SERIALIZER TESTS =====
        
        def test_author_with_nested_books(self):
            """Test Author serializer includes nested books"""
            url = reverse('author-list')
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Check author data includes books
            author_data = response.data[0]
            self.assertIn('books', author_data)
            self.assertEqual(len(author_data['books']), 2)