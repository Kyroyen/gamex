from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.timezone import now as TimezoneNow

class ApiUser(AbstractUser, PermissionsMixin):
    pass

class Tags(models.Model):
    slug = models.SlugField()

class Blog(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField(max_length = 500)
    creator = models.ForeignKey(
        "ApiUser",
        on_delete = models.CASCADE,
        related_name = "created_by",
    )
    date_created = models.DateTimeField(default = TimezoneNow)
    upvotes = models.ManyToManyField(
        "ApiUser",
        related_name = "blog_upvotes"
    )
    tags_related = models.ManyToManyField(
        "Tags",
        related_name="tags_related",
    )

    @property
    def total_upvotes(self):
        return self.upvotes.count()

class Comment(models.Model):
    content = models.TextField(max_length = 255)
    blog = models.ForeignKey(
        "Blog",
        on_delete = models.SET_NULL,
        null = True,
        related_name = "comments",
    )
    date_created = models.DateTimeField(default = TimezoneNow)
    owner = models.ForeignKey(
        "ApiUser",
        on_delete = models.SET_NULL,
        null = True,
        related_name = "commentor",
    )
