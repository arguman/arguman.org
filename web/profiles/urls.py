from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from profiles.views import (RegistrationView, LoginView, LogoutView,
                            ProfileDetailView, ProfileUpdateView)


urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(template_name="auth/login.html"), name='auth_login'),
    url(r'^logout/$', LogoutView.as_view(), name='auth_logout'),
    url(r'^auth/profile$',ProfileUpdateView.as_view(
        template_name="auth/update.html"), name='auth_profile_update'),
    url(r'^register/$', RegistrationView.as_view(
        template_name="auth/register.html"), name='auth_registration'),
    url(r'^complete/$', TemplateView.as_view(
        template_name="auth/complete.html"), name='auth_registration_complete'),
    url(r'^users/(?P<username>[\w\._-]+)$', ProfileDetailView.as_view(
        template_name="auth/profile.html"), name='auth_profile'),

)