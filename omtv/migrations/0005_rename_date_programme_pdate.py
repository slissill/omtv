# Generated by Django 5.0.4 on 2024-05-06 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omtv', '0004_remove_programme_unique_programme_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programme',
            old_name='date',
            new_name='pdate',
        ),
    ]
