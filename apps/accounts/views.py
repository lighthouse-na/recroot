from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . import forms, models


def profile(request) -> HttpResponse:
    """
    Renders the profile page for the logged-in user.

    This view handles rendering the profile page, displaying the user's
    information and qualification types. It checks that the user is
    viewing their own profile and raises a `PermissionDenied` error if
    they are attempting to view another user's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response object containing the rendered profile page.

    Raises:
        PermissionDenied: If the user tries to access another user's profile.
    """
    template_name = "account/profile.html"
    user = request.user
    types = models.Qualification.QualificationType.choices

    # Check that the user is viewing their own profile
    if request.user != user:
        raise PermissionDenied("You do not have permission to view this profile.")

    context = {
        "user": user,
        "types": types,
    }

    return render(request, template_name, context)


# ***************************************************************************************************
#                                           Experience
# ***************************************************************************************************


def create_experience(request) -> HttpResponse:
    """
    Handles the creation of a new experience entry for the logged-in user.

    This view handles both displaying the experience creation form
    and processing form submissions. If the form is submitted via
    POST and is valid, a new experience record is created and associated
    with the logged-in user. The user is then redirected to the experience
    list page. If the form is accessed via GET, an empty form is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response object containing either the form page
                      (on GET request) or a redirect to the experience list page
                      (on successful POST request).
    """
    if request.method == "POST":
        form = forms.ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data, but don't commit to the database yet
            experience = form.save(commit=False)
            experience.user = request.user  # Associate the experience with the logged-in user
            experience.save()  # Save the experience to the database
            return render(request, "account/experience/list.html")  # Redirect to the experience list page
    else:
        form = forms.ExperienceForm()  # Display an empty form for GET requests

    return render(request, "account/experience/create.html", {"form": form})


def delete_experience(request, experience_id) -> HttpResponse:
    """
    Deletes an experience entry for the logged-in user.

    This view is responsible for deleting an experience entry based on
    the provided experience ID. It checks if the experience exists and
    deletes it. After successful deletion, the user is redirected to the
    experience list page.

    Args:
        request (HttpRequest): The HTTP request object.
        experience_id (int): The ID of the experience to be deleted.

    Returns:
        HttpResponse: A response object that redirects the user to the
                      experience list page after deletion.
    """
    experience = get_object_or_404(models.Experience, id=experience_id)
    experience.delete()  # Delete the experience from the database
    return render(request, "account/experience/list.html")  # Redirect to the experience list page


# ***************************************************************************************************
#                                           Qualification
# ***************************************************************************************************


def create_qualification(request) -> HttpResponse:
    """
    Handles the creation of a new qualification entry for the logged-in user.

    This view handles both displaying the qualification creation form
    and processing form submissions. If the form is submitted via POST
    and is valid, a new qualification record is created and associated
    with the logged-in user. The user is then redirected to the qualification
    list page. If the form is accessed via GET, an empty form is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response object containing either the form page
                      (on GET request) or a redirect to the qualification list page
                      (on successful POST request).
    """
    if request.method == "POST":
        form = forms.QualificationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data but don't commit it to the database yet
            qualification = form.save(commit=False)
            qualification.user = request.user  # Associate the qualification with the logged-in user
            qualification.save()  # Save the qualification to the database
            return render(request, "account/qualification/list.html")  # Redirect to the qualification list page
    else:
        form = forms.QualificationForm()  # Display an empty form for GET requests

    return render(
        request,
        "account/qualification/create.html",
        {"form": form},
    )  # Render the qualification creation page with the form


def delete_qualification(request, qualification_id) -> HttpResponse:
    """
    Deletes a qualification entry for the logged-in user.

    This view is responsible for deleting a qualification entry based
    on the provided qualification ID. It checks if the qualification
    exists and deletes it. After successful deletion, the user is
    redirected to the qualification list page.

    Args:
        request (HttpRequest): The HTTP request object.
        qualification_id (int): The ID of the qualification to be deleted.

    Returns:
        HttpResponse: A response object that redirects the user to the
                      qualification list page after deletion.
    """
    qualification = get_object_or_404(models.Qualification, id=qualification_id)
    qualification.delete()  # Delete the qualification from the database
    return render(request, "account/qualification/list.html")  # Redirect to the qualification list page


# ***************************************************************************************************
#                                           Certification
# ***************************************************************************************************


def create_certification(request) -> HttpResponse:
    """
    Handles the creation of a new certification entry for the logged-in user.

    This view handles both displaying the certification creation form
    and processing form submissions. If the form is submitted via POST
    and is valid, a new certification record is created and associated
    with the logged-in user. The user is then redirected to the certification
    list page. If the form is accessed via GET, an empty form is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response object containing either the form page
                      (on GET request) or a redirect to the certification list page
                      (on successful POST request).
    """
    if request.method == "POST":
        form = forms.CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data, but don't commit to the database yet
            certification = form.save(commit=False)
            certification.user = request.user  # Associate the certification with the logged-in user
            certification.save()  # Save the certification to the database
            return render(request, "account/certification/list.html")  # Redirect to the certification list page
    else:
        form = forms.CertificationForm()  # Display an empty form for GET requests

    return render(
        request, "account/certification/create.html", {"form": form}
    )  # Render the certification creation page with the form


def delete_certification(request, certification_id) -> HttpResponse:
    """
    Deletes a certification entry for the logged-in user.

    This view is responsible for deleting a certification entry based
    on the provided certification ID. It checks if the certification
    exists and deletes it. After successful deletion, the user is
    redirected to the certification list page.

    Args:
        request (HttpRequest): The HTTP request object.
        certification_id (int): The ID of the certification to be deleted.

    Returns:
        HttpResponse: A response object that redirects the user to the
                      certification list page after deletion.
    """
    certification = get_object_or_404(models.Certification, id=certification_id)
    certification.delete()  # Delete the certification from the database
    return render(request, "account/certification/list.html")  # Redirect to the certification list page
