from django.conf import settings


class InternalAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ip = request.META.get("REMOTE_ADDR", "")
        # ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0]
        ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        ip = ip.split(",")[0]

        # Check if IP belongs to internal network
        if any(ip.startswith(prefix) for prefix in settings.INTRANET_IP_RANGES):
            request.is_intranet = True
        else:
            request.is_intranet = False

        return self.get_response(request)
