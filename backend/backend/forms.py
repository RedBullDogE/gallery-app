from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=30)
    email = forms.CharField()
    password = forms.CharField(min_length=6)
