from django.urls import path

from .views import RegisterUserView, LoginUserView, UserView, UserCommentView, UserBlogView, BlogDetail, CommentDetail, TagBlogsList, UserUpvoteView

urlpatterns = [
    path("user/<str:username>/", UserView.as_view(), name="user-view"),
    path("user/<str:username>/comments/",
         UserCommentView.as_view(), name="user-comment-view"),
    path("user/<str:username>/blogs/",
         UserBlogView.as_view(), name="user-blog-view"),
    path("user/<str:username>/upvotes/",
         UserUpvoteView.as_view(), name="user-upvote-view"),
    path("blog/<int:id>/", BlogDetail.as_view(), name="blog-detail"),
    path("blog/<int:id>/comments/", CommentDetail.as_view(), name="comment-detail"),
    path("tags/<slug:tag>/", TagBlogsList.as_view(), name="tags-blog-list"),
]
