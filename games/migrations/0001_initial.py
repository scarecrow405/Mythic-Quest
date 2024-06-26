# Generated by Django 5.0.2 on 2024-04-15 19:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('gold_to_gain', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
