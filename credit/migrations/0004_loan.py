# Generated by Django 5.1.3 on 2024-11-11 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0003_delete_loan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loan_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tenure', models.IntegerField()),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monthly_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('emis_paid_on_time', models.IntegerField(default=0)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit.customer')),
            ],
        ),
    ]