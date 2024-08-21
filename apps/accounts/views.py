from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def profile(request):
    template_name = "account/admin/profile.html"
    user = request.user
    if request.user != user:
        raise PermissionDenied("You do not have permission to view this profile.")

    context = {"user": user}

    return render(request, template_name, context)
