from django.shortcuts import render, redirect
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy



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
        form = UserCreationForm()
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app/register.html')

