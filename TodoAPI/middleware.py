from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request as RestFrameworkRequest
from rest_framework.views import APIView


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response