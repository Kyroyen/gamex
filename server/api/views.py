from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.utils import timezone
# from django.http import
import jwt

from .serializers import ApiUserSerializer, BlogSerializer, CommentSerializer, SelfApiUserSerializer
from .models import ApiUser, Comment, Blog, Tags
from .middleware import AuthenticationCookieMiddleware


class RegisterUserView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ApiUserSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed()
        # user = get_object_or_404(ApiUser, username = username)

        payload = {
            "username": username,
            "exp": timezone.now() + timezone.timedelta(hours=24),
            "iat": timezone.now(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token,
        }

        return response


class UserView(APIView):

    def get(self, request, username):
        print(request.user)
        user = get_object_or_404(ApiUser, username=username)
        serializer = SelfApiUserSerializer(
            user,
            context={
                "request": request
            }) if request.user.username == username else ApiUserSerializer(
                user,
                context={
                    "request": request
                })
        response = Response(data=serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        response.data["editable"] = (user == request.user)
        return response


class UserCommentView(APIView):

    def get(self, request, username):
        comments = request.user.commentor.all()
        print(comments)
        serializer = CommentSerializer(
            comments, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserBlogView(APIView):

    def get(self, request, username):
        serializer = BlogSerializer(get_object_or_404(
            ApiUser, username=username).created_by.all(), many=True, context={"request": request})
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        response["editable"] = "True" if (
            request.user == username) else "False"
        # print(response)
        return response

    def post(self, request, username):
        data = request.data
        data["creator"] = request.user
        blog = BlogSerializer(data=data, context={"request": request})
        if blog.is_valid(raise_exception=True):
            blog.save()
            response = Response(data=blog.data, status=status.HTTP_201_CREATED)
            response.data["editable"] = True
            return response
        return Response(status=status.HTTP_404_NOT_FOUND, exception=True)

class UserUpvoteView(APIView):

    def get(self, request, username):
        serializer = BlogSerializer(get_object_or_404(
            ApiUser, username=username).blog_upvotes.all(), many=True, context={"request": request})
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        response["editable"] = "True" if (
            request.user == username) else "False"
        # print(response)
        return response


class BlogDetail(APIView):

    def get(self, request, id):
        try:
            blog = Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, exception=True)
        serializer = BlogSerializer(blog, context={"request": request})
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        # print(serializer.instance.creator, request.user)
        response.data["editable"] = True if (
            request.user == serializer.instance.creator) else False
        return response
    
    def post(self, request, id):
        try:
            blog = Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, exception=True)
        # print(request.data)
        upvote = True if request.data.pop("upvote", False) else False
        response = Response(data="No Action", status=status.HTTP_100_CONTINUE)
        # print(upvote)
        if upvote:
            blog.upvotes.add(request.user)
            serializer = BlogSerializer(blog, context={"request": request})
            response = Response(data=serializer.data, status=status.HTTP_200_OK)
            # print(serializer.instance.creator, request.user)
            response.data["editable"] = True if (
                request.user == serializer.instance.creator) else False
        return response

class CommentDetail(APIView):

    def get(self, request, id):
        try:
            blog = Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, exception=True)
        serializer = CommentSerializer(
            blog.comments.all(), many=True, context={"request": request})
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        # print(serializer.instance.creator, request.user)
        # response.data["editable"] = True if (request.user==serializer.instance.creator) else False
        return response

    def post(self, request, id):
        try:
            blog = Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, exception=True)
        data = request.data
        data["owner"] = request.user
        data["blog"] = id
        serializer = CommentSerializer(
            data=data,
            context={"request": request},
        )
        # print(data)
        # print(serializer.data)
        if serializer.is_valid():
            # print("inside is_valid")
            # print(serializer.validated_data)
            serializer.save()
            response = Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            response.data["editable"] = True
            return response
        return Response(data=serializer.errors, exception=True, status=status.HTTP_400_BAD_REQUEST)

class TagBlogsList(APIView):

    def get(self, request, tag):
        response = Response(data = {"tag" : tag})
        try:
            tag_object = Tags.objects.get(slug = tag)
            response.data["blogs"] = BlogSerializer(
                tag_object.tags_related.all(),
                many = True, 
                context={"request": request},
                ).data
            response.data["count"] = tag_object.tags_related.count()
        except ObjectDoesNotExist:
            pass
        return response

    