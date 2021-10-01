# Generated by Django 2.2.16 on 2021-09-28 13:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_server', '0003_auto_20210928_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='thumb_media',
        ),
        migrations.AddField(
            model_name='content',
            name='thumb_media_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 13, 26, 43, 53233, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='content',
            name='delete_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 13, 26, 43, 53233, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 13, 26, 43, 53233, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='media',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 13, 26, 43, 53233, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='media',
            name='delete_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 13, 26, 43, 53233, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 13, 26, 43, 53233, tzinfo=utc)),
        ),
    ]
