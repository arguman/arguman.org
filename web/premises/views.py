from django.views.generic import DetailView, TemplateView, CreateView

from premises.models import Contention
from premises.forms import ArgumentCreationForm


class ContentionDetailView(DetailView):
    template_name = "premises/contention_detail.html"
    model = Contention


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        contentions = Contention.objects.featured()
        return super(HomeView, self).get_context_data(
            contentions=contentions, **kwargs)


class ArgumentCreationView(CreateView):
    template_name = "premises/new_contention.html"
    form_class = ArgumentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArgumentCreationView, self).form_valid(form)


class PremiseCreationView(PremiseCreationView):
    template_name = "premises/new_contention.html"
    form_class = ArgumentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PremiseCreationView, self).form_valid(form)
