from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization of Book model instances.
    
    Fields:
    - id, title, publication_year, author (all fields from Book model)
    
    Custom Validation:
    - publication_year: Cannot be in the future
    - Uses current year from datetime.date for validation
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Raises:
            serializers.ValidationError: If publication year is in the future
            
        Returns:
            int: The validated publication year
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization of Author model instances.
    
    Fields:
    - id, name: Basic author information
    - books: Nested BookSerializer for related books
    
    Nested Relationship:
    - books: Uses BookSerializer to serialize all related books dynamically
    - many=True: Author can have multiple books
    - read_only=True: Books are included in serialized output but not used for input
    - The relationship is handled through Django's ORM reverse relation (author.books.all())
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']