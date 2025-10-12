# Social Media API

This is a Django REST Framework project that provides a backend API for a social media platform.  
It includes user registration, login, posts, likes, follows, and notifications functionality.

## Features
- User registration and authentication (JWT)
- CRUD operations for posts
- Like/unlike system
- Follow/unfollow users
- Notifications for post likes and follows
- Modular apps: accounts, posts, notifications

## Tech Stack
- Python 3
- Django 5
- Django REST Framework
- SQLite (development)
- JWT Authentication

## How to Run
1. Clone the repository
2. Navigate to the project folder: `cd social_media_api`
3. Create a virtual environment:  
   `python -m venv .venv`
4. Activate it:  
   - Windows: `.venv\Scripts\activate`
5. Install dependencies:  
   `pip install -r requirements.txt`
6. Apply migrations:  
   `python manage.py migrate`
7. Run the development server:  
   `python manage.py runserver`
