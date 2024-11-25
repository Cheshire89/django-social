from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Profile admin view.'''
    list_display = ['id', 'user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']
