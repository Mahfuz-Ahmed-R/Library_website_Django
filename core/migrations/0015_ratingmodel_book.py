# Generated by Django 5.0.6 on 2024-08-02 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_ratingmodel_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingmodel',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.book'),
        ),
    ]
