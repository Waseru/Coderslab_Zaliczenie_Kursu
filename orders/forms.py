from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, MultipleChoiceField

from orders.models import Order, Product, OrderData
from orders.validators import validate_username, validate_min_value


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

class OrderProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(validators=[validate_min_value]) #walidator coś nie działa hehe
