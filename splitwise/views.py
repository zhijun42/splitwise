from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def hello(request):
    """
    Basic "hello world" endpoint that returns a response to indicate that the API is working.

    Parameters:
        name: Name inserted into the message.

    Returns:
        JsonResponse: A JSON response containing a hello message.
    """
    return JsonResponse(data={"message": "Welcome to my version of Splitwise!"}, status=200)
