from django.urls import path,include

from .views import RegisterUserView, LoginUserView, UserView, BlogDetail
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("sign-up/", RegisterUserView.as_view(), name = "sign-up-user"),
    path("log-in/", LoginUserView.as_view(), name = "login-user"),
    path("", include(("api.logged_in_urls", "logged-in-user-view"), namespace="logged-in-user-view")),
]

urlpatterns += staticfiles_urlpatterns(
    
)