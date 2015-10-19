from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth import views

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
    url(r'^password_reset/$', views.password_reset,
        {'template_name': 'auth/password_reset_form.html',
        'email_template_name': 'auth/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done,
        {'template_name': 'auth/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        {'template_name': 'auth/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete,
        {'template_name': 'auth/password_reset_complete.html'},
        name='password_reset_complete'),
)
