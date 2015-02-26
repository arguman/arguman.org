# -*- coding:utf-8 -*-

import json
from datetime import timedelta
from markdown2 import markdown

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Max, Sum
from django.utils.timezone import now
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, TemplateView, CreateView, View
from django.views.generic.edit import UpdateView
from django.db.models import Count

from blog.models import Post
from premises.utils import int_or_zero
from premises.models import Contention, Premise
from premises.forms import (ArgumentCreationForm, PremiseCreationForm,
                            PremiseEditForm, ReportForm)
from premises.signals import (added_premise_for_premise,
                              added_premise_for_contention,
                              reported_as_fallacy,
                              supported_a_premise)
from premises.templatetags.premise_tags import check_content_deletion
from newsfeed.models import Entry
from profiles.mixins import LoginRequiredMixin
from profiles.models import Profile


class ContentionDetailView(DetailView):
    template_name = "premises/contention_detail.html"
    model = Contention

    def get_context_data(self, **kwargs):
        contention = self.get_object()
        GET = self.request.GET
        view = ("list-view" if GET.get("view") == "list" else "tree-view")
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
        return HttpResponse(json.dumps({
            "nodes": self.build_tree(contention, self.request.user),
        }), content_type="application/json")

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
            "reportable_by_authenticated_user": self.user_can_report(
                premise, user),
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
        result = contention.premises.all().aggregate(
            max_sibling=Max('sibling_count'))
        return result['max_sibling'] <= 1


class HomeView(TemplateView):
    template_name = "index.html"
    tab_class = "featured"

    paginate_by = 20

    def get_context_data(self, **kwargs):
        contentions = self.get_contentions()
        if self.request.user.is_authenticated():
            notifications_qs = self.get_unread_notifications()
            notifications = list(notifications_qs)
            self.mark_as_read(notifications_qs)
        else:
            notifications = None
        return super(HomeView, self).get_context_data(
            next_page_url=self.get_next_page_url(),
            tab_class=self.tab_class,
            notifications=notifications,
            has_next_page=self.has_next_page(),
            announcements=self.get_announcements(),
            contentions=contentions, **kwargs)

    def get_announcements(self):
        return Post.objects.filter(is_announcement=True)

    def get_offset(self):
        return int_or_zero(self.request.GET.get("offset"))

    def get_limit(self):
        return self.get_offset() + self.paginate_by

    def has_next_page(self):
        total = self.get_contentions(paginate=False).count()
        return total > (self.get_offset() + self.paginate_by)

    def get_next_page_url(self):
        offset = self.get_offset() + self.paginate_by
        return '?offset=%(offset)s' % {
            "offset": offset
        }

    def get_unread_notifications(self):
        return (self.request.user
                    .notifications
                    .filter(is_read=False)[:5])

    def mark_as_read(self, notifications):
        pks = notifications.values_list("id", flat=True)
        (self.request.user
             .notifications
             .filter(id__in=pks)
             .update(is_read=True))

    def get_contentions(self, paginate=True):
        contentions = (Contention
                       .objects
                       .featured())

        if paginate:
            contentions = (contentions[self.get_offset(): self.get_limit()])

        return contentions


class NotificationsView(LoginRequiredMixin, HomeView):
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
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        return super(SearchView, self).get_context_data(
            keywords=self.get_keywords(),
            **kwargs
        )

    def get_keywords(self):
        return self.request.GET.get('keywords') or ""

    def get_next_page_url(self):
        offset = self.get_offset() + self.paginate_by
        return '?offset=%(offset)s&keywords=%(keywords)s' % {
            "offset": offset,
            "keywords": self.get_keywords()
        }

    def get_contentions(self, paginate=True):
        keywords = self.request.GET.get('keywords')
        if not keywords or len(keywords) < 2:
            result = Contention.objects.none()
        else:
            result = (Contention
                      .objects
                      .filter(title__icontains=keywords))

            if paginate:
                result = result[self.get_offset():self.get_limit()]

        return result


class NewsView(HomeView):
    tab_class = "news"

    def get_contentions(self, paginate=True):
        contentions = Contention.objects.filter(
            is_published=True)

        if paginate:
            contentions = contentions[self.get_offset():self.get_limit()]

        return contentions


class StatsView(HomeView):
    tab_class = "stats"
    template_name = "stats.html"
    partial_templates = {
        Profile: "stats/profile.html",
        Contention: "stats/contention.html",
        Premise: "stats/premise.html",
    }

    method_mapping = {
        "active_users": "get_active_users",
        "supported_users": "get_supported_users",
        "disgraced_users": "get_disgraced_users",
        "supported_premises": "get_supported_premises",
        "fallacy_premises": "get_fallacy_premises",
        "crowded_contentions": "get_crowded_contentions",
    }

    time_ranges = [7, 30]

    def get_context_data(self, **kwargs):
        return super(StatsView, self).get_context_data(
            stats=self.get_stats_bundle(),
            stats_type=self.get_stats_type(),
            days=self.days,
            **kwargs)

    def get_stats_type(self):
        return self.request.GET.get("what")

    def build_time_filters(self, date_field="date_creation"):
        days = self.request.GET.get("days")

        if not days or days == "all":
            self.days = None
            return {}

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = None

        if not days or days not in self.time_ranges:
            raise Http404()

        self.days = days

        field_expression = "%s__gt" % date_field

        return {
            field_expression: timezone.now() - timedelta(days=days)
        }

    def get_stats_bundle(self):
        stat_type = self.get_stats_type()
        if stat_type not in self.method_mapping:
            raise Http404()
        method = getattr(self, self.method_mapping[stat_type])
        return [{
            "template": self.partial_templates[type(item)],
            "object": item
        } for item in method()]

    def get_active_users(self):
        return Profile.objects.annotate(
            premise_count=Sum("premise"),
        ).filter(
            premise_count__gt=0,
            **self.build_time_filters(date_field="premise__date_creation")
        ).order_by("-premise_count")[:10]

    def get_supported_users(self):
        return Profile.objects.annotate(
            supporter_count=Sum("premise__supporters"),
        ).filter(
            supporter_count__gt=0,
            **self.build_time_filters(date_field="premise__date_creation")
        ).order_by("-supporter_count")[:10]

    def get_disgraced_users(self):
        return Profile.objects.annotate(
            report_count=Sum("premise__reports"),
        ).filter(
            report_count__gt=0,
            **self.build_time_filters(date_field="premise__date_creation")
        ).order_by("-report_count")[:10]

    def get_supported_premises(self):
        return Premise.objects.annotate(
            supporter_count=Sum("supporters"),
        ).filter(
            supporter_count__gt=0,
            **self.build_time_filters(date_field="date_creation")
        ).order_by("-supporter_count")[:50]

    def get_fallacy_premises(self):
        return Premise.objects.annotate(
            report_count=Sum("reports"),
        ).filter(
            report_count__gt=0,
            **self.build_time_filters(date_field="date_creation")
        ).order_by("-report_count")[:10]

    def get_crowded_contentions(self):
        return Contention.objects.annotate(
            premise_count=Sum("premises"),
        ).filter(
            premise_count__gt=0,
            **self.build_time_filters(date_field="date_creation")
        ).order_by("-premise_count")[:10]


class UpdatedArgumentsView(HomeView):
    tab_class = "updated"

    def get_contentions(self, paginate=True):
        contentions = (Contention
                       .objects
                       .filter(is_published=True)
                       .order_by('-date_modification'))

        if paginate:
            contentions = contentions[self.get_offset():self.get_limit()]

        return contentions


class ControversialArgumentsView(HomeView):
    tab_class = "controversial"

    def get_contentions(self, paginate=True):
        last_week = now() - timedelta(days=3)
        contentions = (Contention
                       .objects
                       .annotate(num_children=Count('premises'))
                       .order_by('-num_children')
                       .filter(date_modification__gte=last_week))
        if paginate:
            return contentions[self.get_offset():self.get_limit()]

        return contentions


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


class ArgumentCreationView(LoginRequiredMixin, CreateView):
    template_name = "premises/new_contention.html"
    form_class = ArgumentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ip_address = self.request.META['REMOTE_ADDR']
        response = super(ArgumentCreationView, self).form_valid(form)
        form.instance.update_sibling_counts()
        return response


class ArgumentUpdateView(LoginRequiredMixin, UpdateView):
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


class ArgumentPublishView(LoginRequiredMixin, DetailView):

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        if contention.premises.exists():
            contention.is_published = True
            contention.save()
            messages.info(request, u"Argüman yayına alındı.")
        else:
            messages.info(request, u"Argümanı yayına almadan önce en az 1 "
                                   u"önerme ekleyin.")
        return redirect(contention)


class ArgumentUnpublishView(LoginRequiredMixin, DetailView):

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        contention.is_published = False
        contention.save()
        messages.info(request, u"Argüman yayından kaldırıldı.")
        return redirect(contention)


class ArgumentDeleteView(LoginRequiredMixin, DetailView):

    def get_queryset(self):
        return Contention.objects.filter(user=self.request.user)

    def post(self, request, slug):
        contention = self.get_object()
        if check_content_deletion(contention):
            # remove notification
            Entry.objects.delete(contention.get_newsfeed_type(), contention.id)
            contention.delete()
            messages.info(request, u"Argümanınız silindi.")
            return redirect("home")
        else:
            messages.info(request, u"Argümanınız silinecek durumda değil.")
            return redirect(contention)

    delete = post


class PremiseEditView(LoginRequiredMixin, UpdateView):
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
        return super(PremiseEditView, self).get_context_data(**kwargs)


class PremiseCreationView(LoginRequiredMixin, CreateView):
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
        form.instance.ip_address = self.request.META['REMOTE_ADDR']
        form.save()
        contention.update_sibling_counts()

        if form.instance.parent:
            added_premise_for_premise.send(sender=self,
                                           premise=form.instance)
        else:
            added_premise_for_contention.send(sender=self,
                                              premise=form.instance)

        contention.date_modification = timezone.now()
        contention.save()

        return redirect(contention)

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])

    def get_parent(self):
        parent_pk = self.kwargs.get("pk")
        if parent_pk:
            return get_object_or_404(Premise, pk=parent_pk)


class PremiseSupportView(LoginRequiredMixin, View):
    def get_premise(self):
        premises = Premise.objects.exclude(user=self.request.user)
        return get_object_or_404(premises, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.supporters.add(self.request.user)
        supported_a_premise.send(sender=self, premise=premise,
                                 user=self.request.user)
        return redirect(self.get_contention())

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])


class PremiseUnsupportView(PremiseSupportView):
    def delete(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.supporters.remove(self.request.user)
        return redirect(self.get_contention())

    post = delete


class PremiseDeleteView(LoginRequiredMixin, View):
    def get_premise(self):
        if self.request.user.is_staff:
            premises = Premise.objects.all()
        else:
            premises = Premise.objects.filter(user=self.request.user)
        return get_object_or_404(premises,
                                 pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        premise = self.get_premise()
        premise.delete()
        premise.update_sibling_counts()
        contention = self.get_contention()
        if not contention.premises.exists():
            contention.is_published = False
            contention.save()
        return redirect(contention)

    post = delete

    def get_contention(self):
        return get_object_or_404(Contention, slug=self.kwargs['slug'])


class ReportView(LoginRequiredMixin, CreateView):
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

    def get_initial(self):
        return {
            'contention': self.get_contention(),
            'premise': self.get_premise(),
            'reporter': self.request.user
        }

    def form_valid(self, form):
        contention = self.get_contention()
        premise = self.get_premise()
        form.instance.contention = contention
        form.instance.premise = premise
        form.instance.reporter = self.request.user
        form.save()
        reported_as_fallacy.send(sender=self, report=form.instance)
        return redirect(contention)
