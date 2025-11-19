from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    """
    Форма для оновлення даних акаунта (User)
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма для оновлення профілю (Profile)
    """
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'bio']
        widgets = {
            'avatar': forms.FileInput(),
        }


class ActivationCodeForm(forms.Form):
    """
    Форма для введення 6-значного коду з e-mail
    """
    code = forms.CharField(
        max_length=6,
        min_length=6,
        strip=True,
        widget=forms.TextInput(attrs={'autocomplete': 'one-time-code'}),
        label='Код з e-mail',
    )
