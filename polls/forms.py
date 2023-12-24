from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class GiftForm(forms.Form):
    description = forms.CharField(
        label='Введите описание приза ',
    )
    name = forms.IntegerField(
        label='Введите описание приза ',
    )
