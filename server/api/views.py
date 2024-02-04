from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth import authenticate
from django.utils import timezone
import jwt

from .serializers import ApiUserSerializer,BlogSerializer,CommentSerializer
from .models import ApiUser,Comment,Blog
from .middleware import AuthenticationCookieMiddleware

class RegisterUserView(APIView):
    def post(self, request):
        serializer = ApiUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status = status.HTTP_201_CREATED)
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username = username, password = password)
        if not user:
            raise AuthenticationFailed()
        # user = get_object_or_404(ApiUser, username = username)

        payload = {
            "username" : username,
            "exp" : timezone.now() + timezone.timedelta(hours=24),
            "iat" : timezone.now(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt" : token,
        }

        return response
    
class UserView(APIView):
    
    def get(self, request, username):
        print(request.user)
        serializer = ApiUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    
class CommentView(APIView):

    def get(self, request, username):
        serializer = CommentSerializer(request.user.commentor.all(), many = True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)
    
class BlogView(APIView):

    def get(self, request, username):
        serializer = BlogSerializer(request.user.created_by.all(), many = True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, username):
        if username!=request.user.username:
            raise PermissionDenied("User not same")
        data = request.data
        blog = Blog(**data, creator = request.user)
        blog.save()
        serializer = BlogSerializer(blog)
        return Response(data = serializer.data, status=status.HTTP_201_CREATED)