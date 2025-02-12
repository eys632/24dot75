from django.urls import path
from .views import index, login, signup, logout, admin_request_view

app_name = "user"

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("admin_request/", admin_request_view, name="admin_request"),
]
