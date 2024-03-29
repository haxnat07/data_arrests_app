# Generated by Django 5.0.1 on 2024-01-17 21:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='law_firm',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='preferred_arrest_location',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
