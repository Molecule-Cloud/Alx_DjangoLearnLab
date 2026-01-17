from .models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Retrieve all books written by a specific author."""
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books


def query_books_in_library(library_name):
    """Retrieve all books available in a specific library."""
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books

def query_librarian_for_library(library_name):
    """Retrieve the librarian assigned to a specific library."""
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
    return librarian