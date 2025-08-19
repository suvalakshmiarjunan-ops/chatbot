# newapp/middleware.py
from django.shortcuts import redirect
from newapp.models import Admin

class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or "/"

        # Don’t block login, logout, or static/media
        allowlist = ("/login", "/logout", "/static/", "/media/",'/get_message','/send_whatsapp_message')

        # Check if path is protected
        if not path.startswith(allowlist):
            admin_id = request.session.get("admin_id")
            if not admin_id or not Admin.objects.filter(id=admin_id).exists():
                return redirect("/login_view")

        return self.get_response(request)
