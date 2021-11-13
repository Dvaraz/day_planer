import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Note(models.Model):
    """ Note what to do """

    STATUS = (
        (0, 'Active'),
        (1, 'Postponed'),
        (2, 'Done'),
    )

    title = models.CharField(max_length=128, verbose_name="Title")
    message = models.TextField(default="", verbose_name="Message")
    date_add = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=1), verbose_name="Creation time")
    public = models.BooleanField(default=False, verbose_name="Post")
    important = models.BooleanField(default=False, verbose_name='Important')
    author = models.ForeignKey(User, related_name="authors", on_delete=models.PROTECT)
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='Status')

    def __str__(self):
        return f'{self.title}: {self.date_add or "No comments"}'


class Comment(models.Model):
    title = models.CharField(max_length=128, verbose_name='comment_title')
    text = models.TextField(default="", verbose_name="comment_text")
    date_add = models.DateTimeField(auto_now_add=True, verbose_name="comment_time_add")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
