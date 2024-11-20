from django import forms


class LoginForm(forms.Form):
    '''User login form.'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)