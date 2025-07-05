from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Signalement, Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLES, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]



class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ["titre", "description", "categorie","statut","photo", "latitude", "longitude"]
