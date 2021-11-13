from django.contrib.auth.models import User
from rest_framework.serializers import IntegerField, Serializer, ModelSerializer, ListField, ChoiceField, SlugRelatedField, SerializerMethodField

from .models import Note, Comment


class AuthorSerializer(ModelSerializer):
    """ Note author"""
    class Meta:
        model = User
        fields = ('id', 'username',)


class NoteEditorSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['author', ]


class CommentsSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    # Меняем название параметра в ответе
    comment_id = SerializerMethodField('get_comment_id')

    def get_comment_id(self, obj):
        return obj.pk

    class Meta:
        model = Comment
        fields = ('comment_id', 'title', 'text', 'date_add', 'author', )


class NotesSerializer(ModelSerializer):
    """ All notes"""

    author = SlugRelatedField(slug_field='username', read_only=True)
    comment = CommentsSerializer(many=True, read_only=True)

    status = SerializerMethodField('get_status')

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Note
        fields = ['title', 'message', 'date_add', 'public', 'important', 'author', 'status', 'comment', ]


class NoteDetailSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    # comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        exclude = ('public', )


class NoteMiniSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', )


class CommentAddSerializer(ModelSerializer):
    """ Добавление комментария """
    author = AuthorSerializer(read_only=True)
    note = NoteMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_add', 'author', 'note']


class QuerySerializer(Serializer):
    status = ListField(child=ChoiceField(choices=Note.STATUS), required=False)
    important = ListField(child=IntegerField(min_value=0, max_value=1), required=False)
    public = ListField(child=IntegerField(min_value=0, max_value=1), required=False)