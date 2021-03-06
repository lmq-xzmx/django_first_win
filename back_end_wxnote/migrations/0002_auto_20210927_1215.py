# Generated by Django 3.2.4 on 2021-09-27 04:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('back_end_wxnote', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note_list',
            old_name='create_time',
            new_name='talk_time',
        ),
        migrations.AddField(
            model_name='note_list',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]
