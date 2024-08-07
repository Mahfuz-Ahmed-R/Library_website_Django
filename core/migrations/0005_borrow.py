# Generated by Django 5.0.6 on 2024-08-01 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('core', '0004_book_available_copies'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.useraccountmodel')),
            ],
        ),
    ]
