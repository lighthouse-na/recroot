from django.shortcuts import render


def profile(request):
    template_name = "account/admin/profile.html"
    user = request.user
    context = {"user": user}
    return render(request, template_name, context)
