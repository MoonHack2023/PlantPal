# Generated by Django 4.1.5 on 2023-02-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_light_blue_light_green_light_violet_light_yellow_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plants',
            fields=[
                ('plant_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('optemp', models.CharField(max_length=50)),
                ('ophumid', models.CharField(max_length=50)),
                ('opco2', models.CharField(max_length=50)),
                ('optvoc', models.CharField(max_length=50)),
                ('oplight', models.CharField(max_length=50)),
            ],
        ),
    ]
