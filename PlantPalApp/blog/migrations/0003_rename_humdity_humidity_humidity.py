# Generated by Django 4.1.5 on 2023-01-26 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_humidity_time_alter_temp_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='humidity',
            old_name='humdity',
            new_name='humidity',
        ),
    ]
