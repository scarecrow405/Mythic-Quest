# Generated by Django 5.0.2 on 2024-02-26 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_rename_username_character_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='nickname',
            field=models.CharField(max_length=13),
        ),
    ]
