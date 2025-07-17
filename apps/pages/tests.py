import pytest
from django.urls import reverse

from apps.recruitment.models import Vacancy


@pytest.mark.django_db
def test_homepage_vacancies_h1_tag(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert "Vacancies" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_footer_links(client):
    required_links = [
        "https://telecom.na",
        "https://www.telecom.na/privacy-policy",
        "https://www.facebook.com/TelecomNamibia/",
        "https://twitter.com/TelecomNamibia",
        "https://www.linkedin.com/company/telecomnamibiaofficial/",
        "https://www.instagram.com/telecomnamibia/",
    ]

    static_urls = [reverse("home")]
    dynamic_urls = [
        reverse("recruitment:vacancy_detail", kwargs={"slug": vacancy.slug}) for vacancy in Vacancy.objects.all()
    ]

    urls_to_test = static_urls + dynamic_urls

    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "</footer>" in content

        # Check for required links
        for link in required_links:
            assert link in content
