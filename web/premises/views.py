# -*- coding:utf-8 -*-

import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView, CreateView, View
from django.views.generic.edit import UpdateView

from premises.models import Contention, Premise
from premises.forms import ArgumentCreationForm, PremiseCreationForm, PremiseEditForm


class ContentionDetailView(DetailView):
    template_name = "premises/contention_detail.html"
    model = Contention

    def get_context_data(self, **kwargs):
        contention = self.get_object()
        edit_mode = contention.user == self.request.user
        return super(ContentionDetailView, self).get_context_data(
            path=contention.get_absolute_url(),
            edit_mode=edit_mode,
            **kwargs)


class ContentionJsonView(DetailView):
    model = Contention

    def render_to_response(self, context, **response_kwargs):
        contention = self.get_object(self.get_queryset())
        return HttpResponse(json.dumps({
            "nodes": self.build_tree(contention),
        }), content_type="application/json")

    def build_tree(self, contention):
        return {
            "name": contention.title,
            "parent": None,
            "pk": contention.pk,
            "owner": contention.owner,
            "sources": contention.sources,
            "children": self.get_premises(contention)
        }

    def get_premises(self, contention, parent=None):
        children = [{
            "pk": premise.pk,
            "name": premise.text,
            "parent": parent.text if parent else None,
            "sources": premise.sources,
            "premise_type": premise.premise_class(),
            "children": (self.get_premises(contention, parent=premise)
                         if premise.published_children().exists() else [])
        } for premise in contention.published_premises(parent)]
        return children


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


class ArgumentUpdateView(UpdateView):
    template_name = "premises/edit_contention.html"
    form_class = ArgumentCreationForm

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArgumentUpdateView, self).form_valid(form)


class ArgumentPublishView(DetailView):

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        contention.is_published = True
        contention.save()
        messages.info(request, u"Argüman yayına alındı.")
        return redirect(contention)


class ArgumentUnpublishView(DetailView):

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        contention.is_published = False
        contention.save()
        messages.info(request, u"Argüman yayından kaldırıldı.")
        return redirect(contention)


class ArgumentDeleteView(DetailView):

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        contention.delete()
        messages.info(request, u"Argümanınız silindi.")
        return redirect("home")

    delete = post


class PremiseEditView(UpdateView):
    template_name = "premises/edit_premise.html"
    form_class = PremiseEditForm

    def get_queryset(self):
        return Premise.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        return super(PremiseEditView, self).get_context_data(
            #contention=self.get_contention(),
            **kwargs)

    #def get_contention(self):
    #    return get_object_or_404(Contention, slug=self.kwargs['slug'])


class PremiseCreationView(CreateView):
    template_name = "premises/new_premise.html"
    form_class = PremiseCreationForm

    def get_context_data(self, **kwargs):
        return super(PremiseCreationView, self).get_context_data(
            contention=self.get_contention(),
            **kwargs)

    def form_valid(self, form):
        contention = self.get_contention()
        form.instance.user = self.request.user
        form.instance.argument = contention
        form.instance.parent = self.get_parent()
        form.instance.is_approved = contention.user == self.request.user
        form.save()
        return redirect(contention)

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])

    def get_parent(self):
        parent_pk = self.kwargs.get("pk")
        if parent_pk:
            return get_object_or_404(Premise, pk=parent_pk)


class PremiseDeleteView(View):
    def get_premise(self):
        return get_object_or_404(Premise,
                                 user=self.request.user,
                                 pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        contention = self.get_premise()
        contention.delete()
        return redirect(self.get_contention())

    post = delete

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])
