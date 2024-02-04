from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.urls import resolve
import jwt

from .models import ApiUser


class AuthenticationCookieMiddleware(object):
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request, **kwargs):
        # request = kwargs["request"

        if "logged-in" in resolve(request.path).namespaces:
            token = request.COOKIES.get("jwt")
            if not token:
                raise AuthenticationFailed("Unauthenticated-0!")
            
            try:
                payload = jwt.decode(token, "secret", algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthenticated-1!")

            request.user = get_object_or_404(ApiUser, username = payload["username"])

        response = self.get_response(request)

        return response
