from django.urls import path,include

from .views import RegisterUserView, LoginUserView, UserView, BlogDetail

urlpatterns = [
    path("sign-up/", RegisterUserView.as_view(), name = "sign-up-user"),
    path("log-in/", LoginUserView.as_view(), name = "login-user"),
    path("", include(("api.logged_in_urls", "logged-in-user-view"), namespace="logged-in-user-view")),
]