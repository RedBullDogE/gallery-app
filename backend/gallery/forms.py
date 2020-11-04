from django import forms
from .models import Picture

class PictureForm(forms.Form):
    author = forms.IntegerField()
    description = forms.CharField(max_length=1000)
    file = forms.ImageField()

