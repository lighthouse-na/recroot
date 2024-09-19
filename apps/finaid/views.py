from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import FinancialAssistanceApplicationForm
from .models import FinancialAssistanceAdvert, FinancialAssistanceApplication


class FinancialAssistanceApplicationCreateView(CreateView):
    model = FinancialAssistanceApplication
    form_class = FinancialAssistanceApplicationForm
    template_name = "recruitment/finaid/create.html"
    success_url = reverse_lazy("Staff:index")

    def form_valid(self, form):
        advert_id = self.kwargs.get("advert_id")
        advert = get_object_or_404(FinancialAssistanceAdvert, pk=advert_id)
        form = form.save(commit=False)
        form.applicant = self.request.user.profile
        form.advert = advert
        form.save()
        return super().form_valid(form)
