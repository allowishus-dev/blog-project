# Generated by Django 2.2.5 on 2019-10-08 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0002_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivation',
            name='activation_key',
            field=models.CharField(max_length=282),
        ),
    ]