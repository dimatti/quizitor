# Generated by Django 2.2.12 on 2020-05-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('login', models.TextField(max_length=255, unique=True, verbose_name='Login')),
                ('name', models.TextField(max_length=255, unique=True, verbose_name='Name')),
                ('surname', models.TextField(max_length=255, unique=True, verbose_name='Surname')),
                ('current_city', models.TextField(max_length=255, unique=True, verbose_name='City')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-id'],
            },
        ),
    ]
