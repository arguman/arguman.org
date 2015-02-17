import json

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import FormView, CreateView, RedirectView, DetailView, UpdateView
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from profiles.mixins import LoginRequiredMixin
from profiles.forms import RegistrationForm, ProfileUpdateForm
from profiles.models import Profile
from profiles.signals import follow_done, unfollow_done
from premises.models import Contention, Report

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
            is_followed = self.request.user.following.filter(pk=user.id).exists()
        else:
            is_followed = False
        return super(ProfileDetailView, self).get_context_data(
            can_follow=can_follow,
            is_followed=is_followed,
            contentions=contentions)

    @method_decorator(login_required)
    def delete(self, request, **kwargs):
        """
        - Removes `FollowedProfile` object for authenticated user.
        - Fires unfollow_done signal
        """
        user = self.get_object()

        if not request.user.following.filter(id=user.id).exists():
            return HttpResponse(json.dumps({
                "error": _("Takibi birakmadan once takip etmen gerekiyor."),
                "success": False
            }))

        request.user.following.remove(user)

        unfollow_done.send(sender=self, follower=request.user, following=user)

        return HttpResponse(json.dumps({
            "success": True
        }))

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        """
        - Creates `FollowedProfile` object for authenticated user.
        - Fires follow_done signal
        """
        user = self.get_object()

        if user.id == self.request.user.id:
            return HttpResponse(json.dumps({
                "error": _("Kedini takip edemezsin."),
                "success": False
            }))

        if user.followers.filter(pk=request.user.pk).exists():
            return HttpResponse(json.dumps({
                "error": _("Zaten bu kullaniciyi takip ediyorsun"),
                "success": False
            }))

        request.user.following.add(user)

        follow_done.send(sender=self, follower=request.user, following=user)

        return HttpResponse(json.dumps({
            "success": True
        }))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("auth_profile", args=[self.request.user.username])
