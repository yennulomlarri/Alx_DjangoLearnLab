from django.db import models
from django.contrib.auth.models import User

# 1. Author model
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 2. Book model (ForeignKey to Author)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} by {self.author.name}"


# 3. Profile model (OneToOne with User)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# 4. ReaderGroup (ManyToMany with Profile)
class ReaderGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile, related_name="groups")

    def __str__(self):
        return self.name
