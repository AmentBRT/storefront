# Generated by Django 5.0.6 on 2024-06-17 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TagItem',
            new_name='TaggedItem',
        ),
    ]
