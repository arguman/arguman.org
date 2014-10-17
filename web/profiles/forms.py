from django.contrib.auth.forms import UserCreationForm
from profiles.models import Profile


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        model = Profile
