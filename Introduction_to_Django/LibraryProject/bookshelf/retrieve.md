retrieve Book Instance

book = Book.objects.get(title="1984")
print(book.title)
print(book.author)
print(book.publication_year)

<!-- Output
1984
George Orwell
1949 -->
