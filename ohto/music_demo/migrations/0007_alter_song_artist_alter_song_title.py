# Generated by Django 4.0 on 2022-11-22 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_demo', '0006_alter_playlist_cover_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
