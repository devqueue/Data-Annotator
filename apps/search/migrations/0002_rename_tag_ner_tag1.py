# Generated by Django 4.0.2 on 2022-11-21 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ner',
            old_name='tag',
            new_name='tag1',
        ),
    ]
