from django.http import JsonResponse
from django.conf import settings

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(settings.MEDIA_URL):
            return self.get_response(request)

        if request.path.startswith('/admin/') or request.path.startswith('/api/v1/'):
            return self.get_response(request)

        # Proteksi sisa request lainnya
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Unauthorized'}, status=401)

        if request.user.role != 'admin':
            if request.method not in ['GET'] and not request.path.startswith('/api/v1/comments/'):
                return JsonResponse({'detail': 'Forbidden: Admins only can modify this data.'}, status=403)

        return self.get_response(request)
