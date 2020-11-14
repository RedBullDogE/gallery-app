from django import forms


class PictureForm(forms.Form):
    description = forms.CharField(max_length=1000)
    file = forms.ImageField()


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=30)
    email = forms.CharField()
    password = forms.CharField(min_length=6)
