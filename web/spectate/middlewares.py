from django.http import JsonResponse


class RestExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Handle the exception and create a custom error response
            error_message = "Internal Server Error: " + str(e)
            response = JsonResponse({'error': error_message}, status=500)
        return response


class JsonResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 500 and response.status_code <= 599 and request.META.get('HTTP_ACCEPT', '').lower() == 'application/json':
            return JsonResponse({'error': 'sorry'}, status=response.status_code)
        return response
