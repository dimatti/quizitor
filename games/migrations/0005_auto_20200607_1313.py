# Generated by Django 2.2.12 on 2020-06-07 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_resultcluster_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultcluster',
            name='cluster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Cluster'),
        ),
    ]