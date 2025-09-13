# LibraryProject – Introduction to Django

This project demonstrates my hands-on work with Django, including environment setup, creating a Django app, defining models, performing CRUD operations, integrating the Django admin, and pushing the project to GitHub.

---

## Project Overview

The project consists of a Django app called `bookshelf` inside the `LibraryProject` project. It includes a `Book` model to manage book records with fields for title, author, and publication year. CRUD operations are performed using the Django shell, and the Django admin interface is customized for easy management.

---

## Steps Taken

### Task 0: Django Environment Setup
1. Cloned the GitHub repository `Alx_DjangoLearnLab`.  
2. Created a project folder `Introduction_to_Django`.  
3. Installed Django and verified installation.  
4. Started a new Django project `LibraryProject`.  
5. Ran the development server to confirm setup.

### Task 1: Implementing the Book Model
1. Created a Django app `bookshelf`.  
2. Defined the `Book` model in `bookshelf/models.py`.  
3. Added `'bookshelf'` to `INSTALLED_APPS` in `settings.py`.  
4. Ran migrations (`makemigrations` and `migrate`).  
5. Performed CRUD operations in the Django shell: create, retrieve, update, delete.  
6. Documented CRUD commands in `create.md`, `retrieve.md`, `update.md`, and `delete.md`.

### Task 2: Admin Interface Integration
1. Created a superuser using `python manage.py createsuperuser`.  
2. Registered the `Book` model in `bookshelf/admin.py`.  
3. Customized the admin interface to display title, author, and publication year, and added search and filter features.  
4. Ran the server and verified the `Book` model in the admin interface.

---

## Project Structure

