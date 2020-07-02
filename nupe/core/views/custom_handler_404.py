from django.http import JsonResponse


def custom_handler_404(request, exception):
    """
    Retorna um json informativo caso o endpoint requisitado não exista
    """

    return JsonResponse(data={"detail": "endpoint not found"}, status=404)
