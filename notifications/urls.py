from django.urls import path
from django.http import HttpResponse
from .views import NotificationListView

urlpatterns = [
    # 👇 Default page for /api/notifications/
    path('', lambda request: HttpResponse(
        """
        <h2>Notifications API Endpoints</h2>
        <ul>
            <li><a href="">List Notifications (GET)</a></li>
        </ul>
        """,
        content_type="text/html"
    )),

    path('', NotificationListView.as_view(), name='notification_list'),
]
