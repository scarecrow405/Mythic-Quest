# Generated by Django 5.0.2 on 2024-03-12 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0008_character_max_health'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='gold',
            field=models.IntegerField(default=100),
        ),
    ]
