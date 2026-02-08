from django.db import models



# == Authors Model for creating the Author table in the database == #
class Author(models.Model):
    name = models.CharField(max_length=200)
   
    def __str__(self):
        return self.name
    


 # == Books Model for creating the Book table in the database == #   
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title