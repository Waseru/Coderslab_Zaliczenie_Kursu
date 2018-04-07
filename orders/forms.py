from django import forms
from django.core.exceptions import ValidationError

from orders.validators import validate_username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64,
                               widget=forms.PasswordInput)

class AddUserForm(forms.Form):
    username = forms.CharField(max_length=64, validators=[validate_username])
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['confirm_password']
        if password != password2:
            raise ValidationError('Hasła nie są takie same')