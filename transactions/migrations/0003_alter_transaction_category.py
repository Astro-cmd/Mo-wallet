# Generated by Django 5.0.11 on 2025-04-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(max_length=20),
        ),
    ]
