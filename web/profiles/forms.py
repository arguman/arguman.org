# -*- coding: utf-8 -*-

import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (UserCreationForm, 
    AuthenticationForm as BaseAuthenticationForm)

from profiles.models import Profile
from django.utils.translation import ugettext_lazy as _

class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AuthenticationForm, self).__init__(*args, **kwargs)



class RegistrationForm(UserCreationForm):
    username = forms.RegexField(
        label=_("Username"),
        max_length=30, regex=re.compile(r'^[\w\s-]+$', re.LOCALE),
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'invalid': _("Invalid characters")
        }
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        model = Profile

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            Profile._default_manager.get(username__iexact=username)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class ProfileUpdateForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "notification_email")
        model = Profile

    new_password1 = forms.CharField(label=_("New password"),
                                    required=False,
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=False,
                                    label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return self.cleaned_data

    def save(self, commit=True):
        if self.cleaned_data.get("new_password1"):
            self.instance.set_password(self.cleaned_data['new_password1'])
        return super(ProfileUpdateForm, self).save(commit)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Profile._default_manager.exclude(id=self.instance.id).get(
                username__iexact=username)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Bu isimde bir kullanıcı zaten mevcuttur.')
