# Generated by Django 2.2.16 on 2021-09-30 15:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_server', '0005_auto_20210930_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='thumb_media_url',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 15, 34, 50, 166638, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='content',
            name='delete_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 15, 34, 50, 166638, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 15, 34, 50, 166638, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='media',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 15, 34, 50, 166638, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='media',
            name='delete_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 15, 34, 50, 166638, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 30, 15, 34, 50, 166638, tzinfo=utc)),
        ),
    ]
