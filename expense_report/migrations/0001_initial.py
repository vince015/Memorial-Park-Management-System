# Generated by Django 2.0 on 2018-11-03 07:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('reference_number', models.CharField(blank=True, max_length=256, null=True)),
                ('payee', models.CharField(max_length=256)),
                ('amount', models.FloatField(default=0.0)),
                ('category', models.CharField(choices=[('Salaries', 'Salaries'), ('Commissions', 'Commissions'), ('Petty Cash Replenishment', 'Petty Cash Replenishment'), ('Labor Fees', 'Labor Fees'), ('Professional Fees', 'Professional Fees'), ('Allowance', 'Allowance'), ('Repair & Maintenance', 'Repair and Maintenance'), ('Office Supplies', 'Office Supplies'), ('Transportation', 'Transportation'), ('Electicity', 'Electicity'), ('Utilities', 'Utilities'), ('Miscellaneous', 'Miscellaneous')], default='Salaries', max_length=128)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('payee', models.CharField(max_length=256)),
                ('amount', models.FloatField(default=0.0)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('transaction_type', models.SmallIntegerField(choices=[(1, 'CREDIT'), (-1, 'DEBIT')], default=-1)),
                ('value', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': 'Petty Cash Transaction',
                'verbose_name_plural': 'Petty Cash Transactions',
            },
        ),
    ]
