from django import forms


class PictureForm(forms.Form):
    description = forms.CharField(max_length=1000)
    file = forms.ImageField()
