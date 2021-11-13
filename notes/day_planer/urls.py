from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'notes'

urlpatterns = [
    path('notes/', views.NotesView.as_view(), name='notes'),
    path('note/<int:note_id>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/<int:note_id>/', views.NoteEditorView.as_view(), name='note_editor'),
    path('note/add/', views.NoteEditorView.as_view(), name='note_post'),
    path('about/', views.day_planer_version, name='version'),
]