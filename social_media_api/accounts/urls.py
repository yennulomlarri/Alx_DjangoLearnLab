from django.urls import path
from django.http import HttpResponse
from .views import RegisterView, LoginView, FollowUserView, UnfollowUserView

urlpatterns = [
    # 👇 Default welcome page for /api/accounts/
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
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
