from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.models import User
from scrapbook.forms import BaseForm

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

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(BaseForm):
    '''User edit form controller.'''
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(
            id=self.instance.id
        ).filter(
            email=data
        )
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(BaseForm):
    '''Profile edit form controller.'''
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
            }),
            'photo': forms.FileInput()
        }