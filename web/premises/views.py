# -*- coding:utf-8 -*-

from markdown2 import markdown
from datetime import date, timedelta

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, TemplateView, CreateView, View
from django.views.generic.edit import UpdateView
from django.db.models import Count

from premises.constants import NEWS_CONTENT_COUNT, UPDATED_CONTENT_COUNT
from premises.models import Contention, Premise, SITUATION, OBJECTION, SUPPORT, Report
from premises.forms import ArgumentCreationForm, PremiseCreationForm, PremiseEditForm, ReportForm
from premises.signals import added_premise_for_premise, added_premise_for_contention, reported_as_fallacy
from profiles.models import Profile


class ContentionDetailView(DetailView):
    template_name = "premises/contention_detail.html"
    model = Contention

    def get_context_data(self, **kwargs):
        contention = self.get_object()
        view = ("list-view" if self.request.GET.get("view") == "list"
                            else "tree-view")
        edit_mode = (
                self.request.user.is_superuser or
                self.request.user.is_staff or
                contention.user == self.request.user)
        return super(ContentionDetailView, self).get_context_data(
            view=view,
            path=contention.get_absolute_url(),
            edit_mode=edit_mode,
            **kwargs)


class ContentionJsonView(DetailView):
    model = Contention

    def render_to_response(self, context, **response_kwargs):
        contention = self.get_object(self.get_queryset())
        return JsonResponse({
            "nodes": self.build_tree(contention, self.request.user),
        })

    def build_tree(self, contention, user):
        return {
            "name": contention.title,
            "parent": None,
            "pk": contention.pk,
            "owner": contention.owner,
            "sources": contention.sources,
            "is_singular": self.is_singular(contention),
            "children": self.get_premises(contention, user)
        }

    def get_premises(self, contention, user, parent=None):
        children = [{
            "pk": premise.pk,
            "name": premise.text,
            "parent": parent.text if parent else None,
            "reportable_by_authenticated_user": self.user_can_report(premise, user),
            "report_count": premise.reports.count(),
            "user": {
                "id": premise.user.id,
                "username": premise.user.username,
                "absolute_url": reverse("auth_profile",
                                        args=[premise.user.username])
            },
            "sources": premise.sources,
            "premise_type": premise.premise_class(),
            "children": (self.get_premises(contention, user, parent=premise)
                         if premise.published_children().exists() else [])
        } for premise in contention.published_premises(parent)]
        return children

    def user_can_report(self, premise, user):
        if user.is_authenticated() and user != premise.user:
            return not premise.reported_by(user)

        return False

    def is_singular(self, contention):
        result = (contention
                   .premises
                   .all()
                   .aggregate(max_sibling=Max('sibling_count')))
        return result['max_sibling'] <= 1


class HomeView(TemplateView):
    template_name = "index.html"
    tab_class = "featured"

    def get_context_data(self, **kwargs):
        contentions = self.get_contentions()
        if self.request.user.is_authenticated():
            notifications_qs = self.get_unread_notifications()
            notifications = list(notifications_qs)
            self.mark_as_read(notifications_qs)
        else:
            notifications = None
        return super(HomeView, self).get_context_data(
            tab_class=self.tab_class,
            notifications=notifications,
            contentions=contentions, **kwargs)

    def get_unread_notifications(self):
        return (self.request.user
                    .notifications
                    .filter(is_read=False)
                    [:5])

    def mark_as_read(self, notifications):
        pks = notifications.values_list("id", flat=True)
        (self.request.user
             .notifications
             .filter(id__in=pks)
             .update(is_read=True))

    def get_contentions(self):
        return Contention.objects.featured()


class NotificationsView(HomeView):
    template_name = "notifications.html"

    def get_context_data(self, **kwargs):
        notifications_qs = self.request.user.notifications.all()[:40]
        notifications = list(notifications_qs)
        self.mark_as_read(notifications_qs)
        return super(HomeView, self).get_context_data(
            notifications=notifications,
            **kwargs)


class SearchView(HomeView):
    tab_class = 'search'

    def get_context_data(self, **kwargs):
        return super(SearchView, self).get_context_data(
            keywords=self.request.GET.get('keywords') or "",
            **kwargs
        )

    def get_contentions(self):
        keywords = self.request.GET.get('keywords')
        if not keywords or len(keywords) < 2:
            result = []
        else:
            result = Contention.objects.filter(title__icontains=keywords)
        return result


class NewsView(HomeView):
    tab_class = "news"

    def get_contentions(self):
        return Contention.objects.filter(
            is_published=True)[:NEWS_CONTENT_COUNT]


class UpdatedArgumentsView(HomeView):
    tab_class = "updated"

    def get_contentions(self):
        return (Contention
                .objects
                .filter(is_published=True)
                .order_by('-date_modification')
                [:UPDATED_CONTENT_COUNT])

class ControversialArgumentsView(HomeView):
    tab_class = "controversial"

    def get_contentions(self):
        last_week = now() - timedelta(days=3)
        return (Contention
                .objects
                .annotate(num_children=Count('premises'))
                .order_by('-num_children')
                .filter(date_modification__gte=last_week)
                [:UPDATED_CONTENT_COUNT])


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        content = markdown(render_to_string("about.md"))
        return super(AboutView, self).get_context_data(
            content=content, **kwargs)

class TosView(TemplateView):
    template_name = "tos.html"

    def get_context_data(self, **kwargs):
        content = markdown(render_to_string("tos.md"))
        return super(TosView, self).get_context_data(
            content=content, **kwargs)


class ArgumentCreationView(CreateView):
    template_name = "premises/new_contention.html"
    form_class = ArgumentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(ArgumentCreationView, self).form_valid(form)
        form.instance.update_sibling_counts()
        return response


class ArgumentUpdateView(UpdateView):
    template_name = "premises/edit_contention.html"
    form_class = ArgumentCreationForm

    def get_queryset(self):
        contentions = Contention.objects.all()
        if self.request.user.is_superuser:
            return contentions
        return contentions.filter(user=self.request.user)

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


class PremiseCreationView(CreateView):
    template_name = "premises/new_premise.html"
    form_class = PremiseCreationForm

    def get_context_data(self, **kwargs):
        return super(PremiseCreationView, self).get_context_data(
            contention=self.get_contention(),
            parent=self.get_parent(),
            **kwargs)

    def form_valid(self, form):
        contention = self.get_contention()
        form.instance.user = self.request.user
        form.instance.argument = contention
        form.instance.parent = self.get_parent()
        form.instance.is_approved = True
        form.save()
        contention.update_sibling_counts()

        if form.instance.parent:
            added_premise_for_premise.send(sender=self,
                                           premise=form.instance)
        else:
            added_premise_for_contention.send(sender=self,
                                              premise=form.instance)

        return redirect(contention)

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])

    def get_parent(self):
        parent_pk = self.kwargs.get("pk")
        if parent_pk:
            return get_object_or_404(Premise, pk=parent_pk)


class PremiseDeleteView(View):
    def get_premise(self):
        if self.request.user.is_staff:
            premises = Premise.objects.all()
        else:
            premises = Premise.objects.filter(user=self.request.user)
        return get_object_or_404(premises,
                                 pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        contention = self.get_premise()
        contention.delete()
        contention.update_sibling_counts()
        return redirect(self.get_contention())

    post = delete

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])


class ReportView(CreateView):
    form_class = ReportForm
    template_name = "premises/report.html"

    def get_context_data(self, **kwargs):
        return super(ReportView, self).get_context_data(
            premise=self.get_premise(),
            **kwargs)

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])

    def get_premise(self):
        return get_object_or_404(Premise, pk=self.kwargs['pk'])

    def form_valid(self, form):
        contention = self.get_contention()
        premise = self.get_premise()
        form.instance.contention = contention
        form.instance.premise = premise
        form.instance.reporter = self.request.user
        form.save()
        reported_as_fallacy.send(sender=self, report=form.instance)
        return redirect(contention)
