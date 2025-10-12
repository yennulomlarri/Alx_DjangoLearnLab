from django.urls import path
from django.http import HttpResponse
from .views import RegisterView, LoginView, follow_user, unfollow_user

urlpatterns = [
    # 👇 Add this default welcome message for /api/accounts/
    path('', lambda request: HttpResponse(
        """
        <h2>Accounts API Endpoints</h2>
        <ul>
            <li><a href="register/">Register</a></li>
            <li><a href="login/">Login</a></li>
            <li><a href="follow/1/">Follow User (example)</a></li>
            <li><a href="unfollow/1/">Unfollow User (example)</a></li>
        </ul>
        """,
        content_type="text/html"
    )),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]
