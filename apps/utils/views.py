import re

from django.http import HttpResponse

# Create your views here.


def email_validation(request):
    email = request.POST.get("email")

    if not email:
        return HttpResponse("")

    # Define regex for basic email validation
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        # Customize the response to return a specific error message
        return HttpResponse(
            "<p class='text-red-500 text-xs mt-1'>Invalid: Enter Valid Email</p>"
        )

    # Return empty response if email is valid
    return HttpResponse("")
