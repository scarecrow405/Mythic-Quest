# Generated by Django 5.0.2 on 2024-03-10 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0004_monster_base_gold_gained'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='base_exp_gained',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]