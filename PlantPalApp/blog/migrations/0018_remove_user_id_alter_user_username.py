# Generated by Django 4.1.5 on 2023-02-09 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
