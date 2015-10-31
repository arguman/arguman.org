from django.views.generic import DetailView
from nouns.models import Noun


class NounDetail(DetailView):
    model = Noun
    template_name = "nouns/detail.html"
