# Generated by Django 4.1.5 on 2023-02-11 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_device_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='airVelocity',
            fields=[
                ('time', models.DateTimeField(auto_now=True, primary_key=True, serialize=False)),
                ('velocity', models.FloatField()),
                ('device', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.device')),
            ],
            options={
                'ordering': ('time',),
            },
        ),
    ]
