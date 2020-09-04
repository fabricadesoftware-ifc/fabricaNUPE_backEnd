from django.http import JsonResponse

from nupe.resources.const.messages.custom_handler_404 import ENDPOINT_NOT_FOUND


def custom_handler_404(request, exception):
    """
    Retorna um json informativo caso o endpoint requisitado não exista
    """

    return JsonResponse(data={"detail": ENDPOINT_NOT_FOUND}, status=404)
