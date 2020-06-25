from django.http import JsonResponse


def custom_handler_404(request, exception):
    return JsonResponse(data={"detail": "endpoint not found"}, status=404)
