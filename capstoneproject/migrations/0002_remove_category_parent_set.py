# Generated by Django 2.0.3 on 2018-03-26 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capstoneproject', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_set',
        ),
    ]