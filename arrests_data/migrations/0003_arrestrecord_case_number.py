# Generated by Django 5.0.1 on 2024-01-23 22:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrests_data', '0002_arrestrecord_defendant_lawyer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrestrecord',
            name='case_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
