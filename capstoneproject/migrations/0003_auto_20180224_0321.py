# Generated by Django 2.0.2 on 2018-02-24 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstoneproject', '0002_auto_20180223_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phrase',
            name='word',
        ),
        migrations.AddField(
            model_name='phrase',
            name='word',
            field=models.ManyToManyField(null=True, to='capstoneproject.Word'),
        ),
    ]