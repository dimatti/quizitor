# Generated by Django 2.2.12 on 2020-05-21 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200521_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.TextField(default='', max_length=255, unique=True, verbose_name='Username'),
            preserve_default=False,
        ),
    ]
