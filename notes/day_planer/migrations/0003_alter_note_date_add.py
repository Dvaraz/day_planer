# Generated by Django 3.2.9 on 2021-11-12 23:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('day_planer', '0002_auto_20211113_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 23, 43, 1, 798554, tzinfo=utc), verbose_name='Creation time'),
        ),
    ]
