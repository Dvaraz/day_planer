from django.contrib import admin
from .models import Note
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # readonly_fields = ('date_add',)

    list_display = ('title', 'message', 'date_add', 'author', 'id', 'status', 'important', 'public')

    fields = (('title', 'public'), 'message', 'author', 'date_add', 'status', 'important')

    search_fields = ['title', 'message', ]

    list_filter = ('public', 'author',)