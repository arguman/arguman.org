# -*- coding:utf-8 -*-

import json
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, TemplateView, CreateView, View
from django.views.generic.edit import UpdateView
from markdown2 import markdown

from premises.models import Contention, Premise, SITUATION, OBJECTION, SUPPORT
from premises.forms import ArgumentCreationForm, PremiseCreationForm, PremiseEditForm


class ContentionDetailView(DetailView):
    template_name = "premises/contention_detail.html"
    model = Contention

    def get_context_data(self, **kwargs):
        contention = self.get_object()
        edit_mode = (
                self.request.user.is_superuser or
                contention.user == self.request.user)
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
            "is_singular": self.is_singular(contention),
            "children": self.get_premises(contention)
        }

    def get_premises(self, contention, parent=None):
        children = [{
            "pk": premise.pk,
            "name": premise.text,
            "parent": parent.text if parent else None,
            "user": {
                "username": premise.user.username,
                "absolute_url": reverse("auth_profile",
                                        args=[premise.user.username])
            },
            "sources": premise.sources,
            "premise_type": premise.premise_class(),
            "children": (self.get_premises(contention, parent=premise)
                         if premise.published_children().exists() else [])
        } for premise in contention.published_premises(parent)]
        return children

    def is_singular(self, contention):
        result = (contention
                   .premises
                   .all()
                   .aggregate(max_sibling=Max('sibling_count')))
        return result['max_sibling'] <= 1


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        contentions = Contention.objects.featured()
        return super(HomeView, self).get_context_data(
            contentions=contentions, **kwargs)


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        content = markdown(render_to_string("about.md"))
        return super(AboutView, self).get_context_data(
            content=content, **kwargs)


class ArgumentCreationView(CreateView):
    template_name = "premises/new_contention.html"
    form_class = ArgumentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(ArgumentCreationView, self).form_valid(form)
        self.create_demo_premises(form.instance)
        form.instance.update_sibling_counts()
        return response

    def create_demo_premises(self, instance):
        demo = [
            [SUPPORT, "Bu metin örnektir. Düzenleyiniz",
                      "Buraya bir URL girilebilir"],
        ]
        for (premise_type, text, source) in demo:
            Premise.objects.create(
                argument=instance,
                user=self.request.user,
                premise_type=premise_type,
                text=text,
                sources=source,
                is_approved=True)


class ArgumentUpdateView(UpdateView):
    template_name = "premises/edit_contention.html"
    form_class = ArgumentCreationForm

    def get_queryset(self):
        premises = Premise.objects.all()
        if self.request.user.is_superuser:
            return premises
        return premises.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(ArgumentUpdateView, self).form_valid(form)
        form.instance.update_sibling_counts()
        return response


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
        premises = Premise.objects.all()
        if self.request.user.is_superuser:
            return premises
        return premises.filter(user=self.request.user)
    
    def form_valid(self, form):
        response = super(PremiseEditView, self).form_valid(form)
        form.instance.argument.update_sibling_counts()
        return response

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
        form.instance.is_approved = (
            self.request.user.is_superuser or
            contention.user == self.request.user)
        form.save()
        contention.update_sibling_counts()
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
        contention.update_sibling_counts()
        return redirect(self.get_contention())

    post = delete

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])
