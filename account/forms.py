from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    '''User login form controller.'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    '''User registration form controller.'''
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if(cd['password'] != cd['password2']):
            raise forms.ValidationError("Passwords do not match.")
        return cd['password2']