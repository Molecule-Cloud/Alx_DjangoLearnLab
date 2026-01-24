from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book, Article

# ===== HELPER FUNCTIONS =====
def user_can_view_books(user):
    """Check if user has view permission"""
    return user.has_perm('bookshelf.can_view_book')

def user_can_create_books(user):
    """Check if user has create permission"""
    return user.has_perm('bookshelf.can_create_book')

def user_can_edit_books(user):
    """Check if user has edit permission"""
    return user.has_perm('bookshelf.can_edit_book')

def user_can_delete_books(user):
    """Check if user has delete permission"""
    return user.has_perm('bookshelf.can_delete_book')

def user_can_publish_books(user):
    """Check if user has publish permission"""
    return user.has_perm('bookshelf.can_publish_book')

# ===== PERMISSION-PROTECTED BOOK VIEWS =====

# 1. VIEW ALL BOOKS (requires can_view_book)
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list_view(request):
    """Shows all books - only users with view permission can access"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'can_create': request.user.has_perm('bookshelf.can_create_book'),
        'can_edit': request.user.has_perm('bookshelf.can_edit_book'),
        'can_delete': request.user.has_perm('bookshelf.can_delete_book'),
        'can_publish': request.user.has_perm('bookshelf.can_publish_book'),
    })

# 2. CREATE BOOK (requires can_create_book)
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create_view(request):
    """Create new book - only users with create permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        # ... create book logic
        messages.success(request, 'Book created successfully!')
        return redirect('book-list')
    return render(request, 'bookshelf/book_create.html')

# 3. EDIT BOOK (requires can_edit_book AND object-level check)
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit_view(request, book_id):
    """Edit existing book"""
    book = get_object_or_404(Book, id=book_id)
    
    # Additional check: user can only edit their own unpublished books unless they have publish permission
    if not book.is_published or request.user.has_perm('bookshelf.can_publish_book'):
        if request.method == 'POST':
            book.title = request.POST.get('title')
            book.save()
            messages.success(request, 'Book updated!')
            return redirect('book-list')
        return render(request, 'bookshelf/book_edit.html', {'book': book})
    else:
        return HttpResponseForbidden("You don't have permission to edit published books.")

# 4. DELETE BOOK (requires can_delete_book)
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete_view(request, book_id):
    """Delete book"""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted!')
        return redirect('book-list')
    return render(request, 'bookshelf/book_delete.html', {'book': book})

# 5. PUBLISH BOOK (requires can_publish_book)
@permission_required('bookshelf.can_publish_book', raise_exception=True)
def book_publish_view(request, book_id):
    """Publish/unpublish a book"""
    book = get_object_or_404(Book, id=book_id)
    book.is_published = not book.is_published
    book.save()
    
    status = "published" if book.is_published else "unpublished"
    messages.success(request, f'Book {status}!')
    return redirect('book-list')

# ===== DASHBOARD WITH PERMISSION CHECKS =====
@login_required
def user_dashboard(request):
    """Shows user what they can do based on permissions"""
    user_perms = {
        'can_view': user_can_view_books(request.user),
        'can_create': user_can_create_books(request.user),
        'can_edit': user_can_edit_books(request.user),
        'can_delete': user_can_delete_books(request.user),
        'can_publish': user_can_publish_books(request.user),
    }
    
    return render(request, 'bookshelf/dashboard.html', {
        'user': request.user,
        'permissions': user_perms,
        'groups': request.user.groups.all(),
    })