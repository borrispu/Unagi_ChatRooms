# Generated by Django 3.0.5 on 2020-06-06 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roulette', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('chatroom_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roulette.ChatRoom')),
                ('tags', models.ManyToManyField(to='roulette.Tag')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]