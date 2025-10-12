from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Get content type for Book
        book_content_type = ContentType.objects.get_for_model(Book)

        # Librarians can manage books
        librarian_group, _ = Group.objects.get_or_create(name="Librarians")
        permissions = Permission.objects.filter(content_type=book_content_type)
        librarian_group.permissions.set(permissions)

        # Members can only view books
        member_group, _ = Group.objects.get_or_create(name="Members")
        view_permission = Permission.objects.get(
            codename="view_book",
            content_type=book_content_type
        )
        member_group.permissions.add(view_permission)

        self.stdout.write(self.style.SUCCESS("Groups and permissions created successfully."))
