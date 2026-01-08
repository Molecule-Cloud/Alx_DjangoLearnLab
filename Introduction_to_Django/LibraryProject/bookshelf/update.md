#UPDATE

book = Book.Objects.get(title="1984")

book.title = "Nineteen Eighty-Four"
book.save()

print(Book.Objects.get(id=1).title)
#Nineteen Eighty-Four
