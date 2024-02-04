from django.urls import path

from .views import RegisterUserView, LoginUserView, UserView, CommentView, BlogView

urlpatterns = [
    path("", UserView.as_view(), name = "user-view"),
    path("comments/", CommentView.as_view(), name = "comment-view"),
    path("blogs/", BlogView.as_view(), name = "blog-view"),
]