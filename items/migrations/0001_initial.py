# Generated by Django 5.0.2 on 2024-03-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('effect', models.CharField(choices=[('EXP Boost', 'EXP Boost'), ('Max Health Boost', 'Max Health Boost'), ('Strength Boost', 'Strength Boost'), ('Agility Boost', 'Agility Boost'), ('Damage Boost', 'Damage Boost'), ('Armor Boost', 'Armor Boost'), ('All Stats Boost', 'All Stats Boost')], max_length=100)),
                ('boost_amount_percentage', models.IntegerField(default=0)),
            ],
        ),
    ]
