from django.shortcuts import redirect

class CheckAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != '/login/':
            return redirect('/login/')  # Redirect to the login page if not authenticated
        response = self.get_response(request)
        return response