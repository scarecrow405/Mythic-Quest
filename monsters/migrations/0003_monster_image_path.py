# Generated by Django 5.0.2 on 2024-03-05 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0002_monster_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='image_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
