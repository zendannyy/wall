# Generated by Django 2.2 on 2021-07-09 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0005_auto_20210709_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='liked_by',
            field=models.ManyToManyField(null=True, related_name='messages_liked', to='wall_app.User'),
        ),
    ]
