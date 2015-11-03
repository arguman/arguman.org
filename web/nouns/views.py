from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from nouns.models import Noun, Relation
from nouns.forms import RelationCreationForm
from profiles.mixins import LoginRequiredMixin


class NounDetail(DetailView):
    model = Noun
    template_name = "nouns/detail.html"


class RelationCreate(LoginRequiredMixin, CreateView):
    model = Relation
    template_name = "nouns/new_relation.html"
    form_class = RelationCreationForm
    initial = {
        'relation_type': Relation.HYPERNYM
    }

    def form_valid(self, form):
        form.instance.source = self.get_noun()
        form.instance.target = form.get_target()
        form.instance.user = self.request.user
        form.instance.is_active = False
        form.save()
        return redirect(form.instance.source)

    def get_context_data(self, **kwargs):
        noun = self.get_noun()
        return super(RelationCreate, self).get_context_data(
            noun=noun, **kwargs)

    def get_noun(self):
        return get_object_or_404(Noun, slug=self.kwargs.get('slug'))
