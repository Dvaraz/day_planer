from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render

from django.conf import settings
from .models import Note, Comment
from .serializers import NotesSerializer, QuerySerializer, NoteEditorSerializer, NoteDetailSerializer, CommentsSerializer, CommentAddSerializer


class NotesView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):

        notes = Note.objects.filter(Q(author=request.user) | Q(public=True)).order_by('date_add', '-important', ).select_related('author')

        query_params = QuerySerializer(data=request.query_params)
        if query_params.is_valid():
            # Filter for 3 conditions
            if query_params.data.get('status') and query_params.data.get('important') and query_params.data.get(
                    'public'):
                notes = notes.filter(
                    Q(important__in=query_params.data['important']) & Q(status__in=query_params.data['status'])
                    & Q(public__in=query_params.data['public']))

            if query_params.data.get('status'):
                notes = notes.filter(status__in=query_params.data['status'])

            if query_params.data.get('important') is not None:
                notes = notes.filter(important__in=query_params.data['important'])

            if query_params.data.get('public') is not None:
                notes = notes.filter(public__in=query_params.data['public'])

        else:
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = NotesSerializer(notes, many=True)

        return Response(serializer.data)


class NoteEditorView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        new_note = NoteEditorSerializer(data=request.data)

        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):

        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound(f'Note with id {note_id} for user {request.user} not found')

        note.date_add = timezone.now() + timezone.timedelta(days=1)
        new_note = NoteEditorSerializer(note, data=request.data, partial=True)

        if new_note.is_valid():
            new_note.save()
            return Response(new_note.data, status=status.HTTP_200_OK)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):

        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound('Not found')

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):

        note = Note.objects.filter(pk=note_id, public=True, author=request.user).first()

        if not note:
            raise NotFound(f'Note with id {note_id} not found')

        serializer = NoteDetailSerializer(note)

        return Response(serializer.data)


class CommentDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, note_id):

        note = Note.objects.filter(Q(public=True) & Q(pk=note_id)).first()
        if not note:
            raise NotFound(f'Статья с id={note_id} не найдена')

        new_comment = CommentAddSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save(note=note, author=request.user)
            return Response(new_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = Comment.objects.filter(pk=comment_id, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def day_planer_version(request):
    version = settings.APP_VERSIONS['day_planer']
    user = request.user
    return render(request, 'day_planer/index.html', {'version': version, 'user': user})