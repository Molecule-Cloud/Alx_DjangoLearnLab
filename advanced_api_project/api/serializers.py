from rest_framework import serializers
from .models import Book, Author



# == Serializer for the Book model to convert model instances to JSON and vice versa == #
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def is_not_future_year(self, value):
        if value > 2026:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    

# == Serializer for the Author model to convert model instances to JSON and vice versa == #
class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name']


