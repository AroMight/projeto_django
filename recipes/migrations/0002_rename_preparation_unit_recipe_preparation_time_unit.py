# Generated by Django 5.0.3 on 2024-03-24 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='preparation_unit',
            new_name='preparation_time_unit',
        ),
    ]