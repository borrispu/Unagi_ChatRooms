# Generated by Django 3.0.5 on 2020-06-06 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roulette', '0002_auto_20200606_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='chatroom_name',
            new_name='name',
        ),
    ]
