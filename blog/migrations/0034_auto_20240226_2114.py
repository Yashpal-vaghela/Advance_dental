# Generated by Django 3.2 on 2024-02-26 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_place_schema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='breadcrumb',
        ),
        migrations.RemoveField(
            model_name='place',
            name='canonical',
        ),
        migrations.RemoveField(
            model_name='place',
            name='description',
        ),
        migrations.RemoveField(
            model_name='place',
            name='h1',
        ),
        migrations.RemoveField(
            model_name='place',
            name='image',
        ),
        migrations.RemoveField(
            model_name='place',
            name='keyword',
        ),
        migrations.RemoveField(
            model_name='place',
            name='og_card',
        ),
        migrations.RemoveField(
            model_name='place',
            name='og_site',
        ),
        migrations.RemoveField(
            model_name='place',
            name='og_type',
        ),
        migrations.RemoveField(
            model_name='place',
            name='schema',
        ),
        migrations.RemoveField(
            model_name='place',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='place',
            name='title',
        ),
    ]
