# Generated by Django 2.2.12 on 2020-06-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20200606_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultcluster',
            name='results',
            field=models.ManyToManyField(to='games.ResultPoint'),
        ),
    ]
