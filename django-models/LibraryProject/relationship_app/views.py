from django.shortcuts import render
from .models import Library, Book
from django.views.generic.detail import DetailView
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class BookDetailView(DetailView):
    """"A class-based view for displaying details of a specific library, listing all books available in that library"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        return context


