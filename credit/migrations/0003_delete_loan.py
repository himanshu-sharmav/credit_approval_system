# Generated by Django 5.1.3 on 2024-11-11 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0002_customer_age'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Loan',
        ),
    ]