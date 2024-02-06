from django.shortcuts import get_object_or_404,redirect
from rest_framework.exceptions import AuthenticationFailed
from django.urls import resolve
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
import jwt

from .models import ApiUser


class AuthenticationCookieMiddleware(object):
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request, **kwargs):
        # request = kwargs["request"

        try:
            if "logged-in-user-view" in resolve(request.path).namespaces:
                token = request.COOKIES.get("jwt")
                if not token:
                    raise AuthenticationFailed("Unauthenticated-0!")
                
                try:
                    payload = jwt.decode(token, "secret", algorithms=["HS256"])
                except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed("Unauthenticated-1!")

                request.user = get_object_or_404(ApiUser, username = payload["username"])
        except AuthenticationFailed as AF:
            return redirect("login-user")

        response = self.get_response(request)

        return response
