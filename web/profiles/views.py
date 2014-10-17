import json

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import FormView, CreateView, RedirectView, DetailView

from profiles.forms import RegistrationForm
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


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse("home")


class ProfileDetailView(DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = "profile"
    model = Profile

    def get_context_data(self, **kwargs):
        """
        Adds extra context to template
        """
        user = self.get_object()
        contentions = Contention.objects.filter(user=user)
        can_follow = self.request.user != user
        is_followed = self.request.user.following.filter(pk=user.id).exists()
        return super(ProfileDetailView, self).get_context_data(
            can_follow=can_follow,
            is_followed=is_followed,
            contentions=contentions)

    def delete(self, request, **kwargs):
        """
        - Removes `FollowedProfile` object for authenticated user.
        - Fires unfollow_done signal
        """
        user = self.get_object()

        request.user.following.remove(user)

        unfollow_done.send(sender=self, follower=request.user, following=user)

        return HttpResponse(json.dumps({
            "success": True
        }))

    def post(self, request, **kwargs):
        """
        - Creates `FollowedProfile` object for authenticated user.
        - Fires follow_done signal
        """
        user = self.get_object()

        if user.followers.filter(pk=request.user.pk).exists():
            return HttpResponse(json.dumps({
                "error": "You already following this people."
            }))

        request.user.following.add(user)

        follow_done.send(sender=self, follower=request.user, following=user)

        return HttpResponse(json.dumps({
            "success": True
        }))
