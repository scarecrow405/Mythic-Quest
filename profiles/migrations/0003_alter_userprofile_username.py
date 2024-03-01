# Generated by Django 5.0.2 on 2024-02-26 16:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_userprofile_about_alter_userprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
