from polls import models as md
from django import forms


class Filter(forms.Form):
    username = forms.CharField()


class ImageForm(forms.ModelForm):
    class Meta:
        model = md.Image
        fields = ['Img']

    Img = forms.ImageField(
        label='Изображение',
        widget=forms.FileInput()
    )


class GiftForm(forms.ModelForm):
    class Meta:
        model = md.Gifts
        fields = ['name', 'description', 'Img']
    name = forms.CharField(
        label='Название приза:'
    )
    description = forms.CharField(
        label='Описание приза:'
    )
    Img = forms.ImageField(
        label='Изображение:',
        widget=forms.FileInput()
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


class EditGiftForm(forms.Form):
    name = forms.CharField(
        max_length=20
    )
    description = forms.CharField(
        max_length=200
    )
    Img = forms.ImageField(
        label='Изображение',
        widget=forms.FileInput()
    )




