from django.contrib import admin
from .models import Note, Comment
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # readonly_fields = ('date_add',)

    list_display = ('title', 'message', 'date_add', 'author', 'id', 'status', 'important', 'public')

    fields = (('title', 'public'), 'message', 'author', 'date_add', 'status', 'important')

    search_fields = ['title', 'message', ]

    list_filter = ('public', 'author',)


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    readonly_fields = ('date_add', )
    list_display = ('title', 'text', 'date_add', 'author', 'note', )

    fields = ('title', 'text', 'author', 'date_add', 'note', )

    search_fields = ['title', 'text', ]

    list_filter = ('author', 'date_add')