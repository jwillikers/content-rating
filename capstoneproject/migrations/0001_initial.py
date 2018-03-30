# Generated by Django 2.0.3 on 2018-03-30 14:02

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.SmallIntegerField(choices=[(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')])),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'default_manager_name': 'categories',
            },
            managers=[
                ('categories', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'default_manager_name': 'words',
            },
            managers=[
                ('words', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='WordFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.SmallIntegerField(choices=[(0, 'innocuous'), (1, 'slight'), (2, 'moderate'), (3, 'heavy')])),
                ('strength', models.BooleanField(choices=[(True, 'strong'), (False, 'weak')], default='weak')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capstoneproject.Category')),
            ],
            options={
                'default_manager_name': 'word_features',
            },
            managers=[
                ('word_features', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='word_features',
            field=models.ManyToManyField(to='capstoneproject.WordFeature'),
        ),
    ]
