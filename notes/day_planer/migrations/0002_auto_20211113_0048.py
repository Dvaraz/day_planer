# Generated by Django 3.2.9 on 2021-11-12 21:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('day_planer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('message', models.TextField(default='', verbose_name='Message')),
                ('date_add', models.DateTimeField(default=datetime.datetime(2021, 11, 13, 21, 48, 27, 472772, tzinfo=utc), verbose_name='Creation time')),
                ('public', models.BooleanField(default=False, verbose_name='Post')),
                ('important', models.BooleanField(default=False, verbose_name='Important')),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Postponed'), (2, 'Done')], default=0, verbose_name='Status')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='DayPlaner',
        ),
    ]
