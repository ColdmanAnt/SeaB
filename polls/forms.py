from django import forms


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
