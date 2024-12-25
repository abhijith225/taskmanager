# myapp/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class FakeAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_user = request.headers.get('X-User')

        if not x_user:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        if x_user == 'admin':
            request.user = {'username': 'admin', 'role': 'Admin'}
        elif x_user.startswith('user'):
            request.user = {'username': x_user, 'role': 'User'}
        else:
            return JsonResponse({'error': 'Invalid user'}, status=403)

    def process_response(self, request, response):
        return response
