# Generated by Django 4.1.5 on 2023-01-28 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_plant_alter_humidity_humidity_alter_temp_temp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='humidity',
            name='plant_id',
        ),
        migrations.RemoveField(
            model_name='temp',
            name='plant_id',
        ),
        migrations.DeleteModel(
            name='Plant',
        ),
    ]
