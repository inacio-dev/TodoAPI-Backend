from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request as RestFrameworkRequest
from rest_framework.views import APIView


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # drf_request: RestFrameworkRequest = APIView().initialize_request(request)
        # user = drf_request.user

        # if request.method != "GET" and user.is_anonymous is False:
        #     try:
        #         license = user.get_active_license()
        #     except License.DoesNotExist:
        #         return JsonResponse(
        #             data={"error": ["Você não tem uma licença válida"]},
        #             status=status.HTTP_402_PAYMENT_REQUIRED,
        #         )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response