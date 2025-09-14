# Delete Operation

```python
from bookshelf.models import Book

# Delete the book
book.delete()

# Verify deletion
Book.objects.all()
# Output: <QuerySet []>

