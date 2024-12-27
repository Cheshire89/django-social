from django.contrib import admin
from .models import Profile, Contact

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Profile admin view.'''
    list_display = ['id', 'user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    '''Contact admin view.'''
    list_display = ['id', 'user_from', 'user_to']
