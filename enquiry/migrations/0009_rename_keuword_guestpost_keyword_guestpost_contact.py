# Generated by Django 4.0.4 on 2022-09-18 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0008_remove_blogplanmytour_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guestpost',
            old_name='keuword',
            new_name='keyword',
        ),
        migrations.AddField(
            model_name='guestpost',
            name='contact',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
