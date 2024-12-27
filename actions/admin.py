from django.contrib import admin
from .models import Action

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','verb','created','target_ct','target_id','target']
    list_filter = ['created']
    search_fields = ['verb']
