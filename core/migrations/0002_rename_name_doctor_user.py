# Generated by Django 5.1.3 on 2024-11-26 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='name',
            new_name='user',
        ),
    ]
