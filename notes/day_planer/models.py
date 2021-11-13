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
        return f'{self.get_status_display()}: {self.date_add or "No comments"}'