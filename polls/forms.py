from polls import models as md
from django import forms


class ImageForm(forms.ModelForm):
    class Meta:
        model = md.Image
        fields = ['Img']

    Img = forms.ImageField(
        label='Изображение',
        widget=forms.FileInput()
    )


class GiftForm(forms.Form):
    description = forms.CharField(
        label='Введите описание приза ',
        max_length=200
    )
    name = forms.CharField(
        label='Введите описание приза ',
        max_length=20
    )


class BoardForm(forms.Form):
    name = forms.CharField(
        label='Введите описание приза ',
        max_length=20
    )
    size = forms.IntegerField(
        label='Введите размеры приза',
        max_value=12,
        min_value=4
    )


class EditForm(forms.Form):
    number = forms.IntegerField(
        label='Введите id поля которого хотите редактировать',
    )


class ShipForm(forms.Form):
    x = forms.IntegerField()
    y = forms.IntegerField()
    gift_id = forms.IntegerField()


class ShotForm(forms.Form):
    shots = forms.IntegerField()
    user = forms.IntegerField()


class BattleForm(forms.Form):
    x = forms.IntegerField()
    y = forms.IntegerField()
