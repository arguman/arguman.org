import json

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import (
    FormView, CreateView, RedirectView, DetailView, UpdateView)
from django.db.models import Q

from profiles.mixins import LoginRequiredMixin
from profiles.forms import RegistrationForm, ProfileUpdateForm
from profiles.models import Profile
from profiles.signals import follow_done, unfollow_done
from premises.models import Contention


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "auth/register.html"

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password1"])
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse("home")


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("home")

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        return context


class LogoutView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse("home")


class ProfileDetailView(DetailView):
    slug_field = 'username__iexact'
    slug_url_kwarg = 'username'
    context_object_name = "profile"
    model = Profile

    def get_context_data(self, **kwargs):
        """
        Adds extra context to template
        """
        user = self.get_object()
        contentions = Contention.objects.filter(
            Q(premises__user=user) | Q(user=user)
        ).distinct()

        if self.request.user != user:
            contentions = contentions.filter(is_published=True)

        can_follow = self.request.user != user

        if self.request.user.is_authenticated():
            is_followed = self.request.user.following.filter(
                pk=user.id).exists()
        else:
            is_followed = False
        return super(ProfileDetailView, self).get_context_data(
            can_follow=can_follow,
            is_followed=is_followed,
            contentions=contentions)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("auth_profile", args=[self.request.user.username])
