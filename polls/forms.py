from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class GiftForm(forms.Form):
    description = forms.CharField(
        label='Введите описание приза ',
        max_length=200
    )
    name = forms.CharField(
        label='Введите описание приза ',
        max_length=20
    )
