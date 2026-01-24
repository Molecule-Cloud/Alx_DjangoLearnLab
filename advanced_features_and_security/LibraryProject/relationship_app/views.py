from django.shortcuts import render, redirect
from .models import Library, Book, Author
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import get_user_model



# === ROLE CHECKING HELPERS === #
def admin_required(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin()

def librarian_required(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_librarian() 

def member_required(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_member()



# === Views for Libraries and Books === #

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """"A class-based view for displaying details of a specific library, listing all books available in that library"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        return context



# === User Authentication Views === #

# UserLogin View

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
        else:
            form = AuthenticationForm()
        return render(request, 'relationship_app/login.html', {'form': form})

 # UserLogout View   
def LogoutView(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

@login_required
def ProtectedView(request):
    return render(request, 'relationship_app/protected.html', {'user': request.user})




#User Registration View

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = user.profile
            profile.role = 'MEMBER'
            profile.save()

            login(request, user)
            return redirect('relationship_app/register.html')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})





# === ROLE-BASED ACCESS CONTROL VIEWS === #

@user_passes_test(admin_required)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(librarian_required, login_url='relationship_app/login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(member_required, login_url='relationship_app/login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')



# === Permission-Based Access Control Views === #

@permission_required('relationship_app.can_add_book', login_url='relationship_app/login')
def add_book_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')

        author = Author.objects.get(id=author_id)
        book = Book.objects.create(title=title, author=author)
        return redirect('relationship_app/book-list')
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@permission_required('relationship_app.can_change_book', login_url='relationship_app/login')
def edit_book_view(request, book_id):
    book = Book.objects_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author_id = request.POST.get('author_id')
        book.save()
        return redirect('relationship_app/book-list')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

@permission_required('relationship_app.can_delete_book', login_url='relationship_app/login')
def delete_book_view(request, book_id):
    book = Book.objects_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app/book-list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

@login_required
def manage_books_view(request):
    can_add = request.user.has_perm('relationship_app.can_add_book') 
    can_change = request.user.has_perm('relationship_app.can_change_book')
    can_delete = request.user.has_perm('relationship_app.can_delete_book')

    context = {
        'can_add': can_add,
        'can_change': can_change,
        'can_delete': can_delete,
        'books': Book.objects.all() if can_change or can_delete else []
    }
    return render(request, 'relationship_app/manage_books.html', context)