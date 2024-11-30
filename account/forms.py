from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.utils.safestring import SafeString

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


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group mb-3'>"))


class UserEditForm(BaseForm):
    '''User edit form controller.'''
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


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