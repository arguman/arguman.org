from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from profiles.models import Profile
import re

class RegistrationForm(UserCreationForm):
    username = forms.RegexField(
        label="kullanıcı adın", max_length=30, regex=re.compile(r'^[\w\s-]+$', re.A),
        help_text = "30 karakterden az, ascii, - ve boşluk kullanabileceginiz kullanıcı adı",
        error_messages = {'invalid': "ascii, - boşluk karakterleri dışında karakter girmeyiniz."}
        )
        
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        model = Profile


    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            Profile._default_manager.get(username=username)
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
        fields = ("username", "email")
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
