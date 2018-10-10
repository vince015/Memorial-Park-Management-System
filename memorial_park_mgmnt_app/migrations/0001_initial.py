# Generated by Django 2.0 on 2018-10-10 14:42

import datetime
from django.db import migrations, models
import django.db.models.deletion
import memorial_park_mgmnt_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=56)),
                ('first_name', models.CharField(max_length=56)),
                ('middle_name', models.CharField(blank=True, max_length=56, null=True)),
                ('rank', models.CharField(choices=[('SALES_AGENT', 'Sales Agent'), ('UNIT_MNGR', 'Unit Manager'), ('SALES_LEADER', 'Sales Leader'), ('REFERENT', 'Referent')], default='SALES_AGENT', max_length=56)),
                ('mobile', models.CharField(blank=True, max_length=18, null=True)),
                ('landline', models.CharField(blank=True, max_length=18, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('house_number', models.CharField(blank=True, max_length=8, null=True)),
                ('street', models.CharField(blank=True, max_length=128, null=True)),
                ('barangay', models.CharField(blank=True, max_length=128, null=True)),
                ('town', models.CharField(blank=True, max_length=128, null=True)),
                ('province', models.CharField(blank=True, max_length=128, null=True)),
                ('valid_id', models.FileField(blank=True, null=True, upload_to=memorial_park_mgmnt_app.models.valid_id_directory_path)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('other_address', models.CharField(blank=True, max_length=512, null=True)),
                ('business_name', models.CharField(blank=True, max_length=512, null=True)),
                ('business_address', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start', models.DateField(default=datetime.date.today)),
                ('end', models.DateField(default=datetime.date.today)),
                ('issue_date', models.DateField(default=datetime.date.today)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('amount_due', models.FloatField(default=0.0)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('PAID', 'Paid'), ('OVERDUE', 'Overdue')], default='NEW', max_length=64)),
                ('remarks', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('group', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group')),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=56)),
                ('first_name', models.CharField(max_length=56)),
                ('middle_name', models.CharField(blank=True, max_length=56, null=True)),
                ('mobile', models.CharField(blank=True, max_length=18, null=True)),
                ('landline', models.CharField(blank=True, max_length=18, null=True)),
                ('house_number', models.CharField(blank=True, max_length=8, null=True)),
                ('street', models.CharField(blank=True, max_length=128, null=True)),
                ('barangay', models.CharField(max_length=128)),
                ('town', models.CharField(max_length=128)),
                ('province', models.CharField(max_length=128)),
                ('valid_id', models.FileField(blank=True, null=True, upload_to=memorial_park_mgmnt_app.models.valid_id_directory_path)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('other_address', models.CharField(blank=True, max_length=512, null=True)),
                ('business_name', models.CharField(blank=True, max_length=512, null=True)),
                ('business_address', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='memorial_park_mgmnt_app.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=256, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('buyer_type', models.CharField(choices=[('PRE-NEED', 'Pre-Need'), ('AT-NEED', 'At-Need')], default='PRE-NEED', max_length=32)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('REVIEWED', 'Reviewed'), ('FORFEITED', 'Forfeited')], default='NEW', max_length=64)),
                ('remarks', models.CharField(blank=True, max_length=256, null=True)),
                ('reservation', models.FloatField(default=0.0)),
                ('payment_terms', models.CharField(choices=[('SPOT', 'Spot'), ('INSTALLMENT', 'Installment')], default='SPOT', max_length=256)),
                ('sold_by', models.CharField(choices=[('SALES_AGENT', 'Sales Agent'), ('UNIT_MNGR', 'Unit Manager'), ('SALES_LEADER', 'Sales Leader'), ('REFERENT', 'Referent')], default='SALES_AGENT', max_length=32)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_contracts', to='memorial_park_mgmnt_app.Client')),
            ],
        ),
        migrations.CreateModel(
            name='DownpaymentPromo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('split', models.PositiveSmallIntegerField(default=1)),
                ('discount', models.FloatField(default=0.0)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(default=memorial_park_mgmnt_app.models.one_year_from_today)),
            ],
        ),
        migrations.CreateModel(
            name='InstallmentOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('split', models.PositiveSmallIntegerField(default=1)),
                ('discount', models.FloatField(default=0.0)),
                ('months', models.PositiveSmallIntegerField(default=12)),
                ('interest', models.FloatField(default=0.0)),
                ('contract', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='installment_option', to='memorial_park_mgmnt_app.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='InstallmentPromo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('months', models.PositiveSmallIntegerField(default=12)),
                ('interest', models.FloatField(default=0.0)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(default=memorial_park_mgmnt_app.models.one_year_from_today)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.CharField(max_length=32)),
                ('lot', models.CharField(max_length=32)),
                ('unit', models.CharField(max_length=32)),
                ('price', models.FloatField(default=0.0)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lots', to='memorial_park_mgmnt_app.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='LotType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_type', models.CharField(default='REG', max_length=32)),
                ('price', models.FloatField(default=0.0)),
                ('vat', models.FloatField(default=0.0)),
                ('care_fund', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=256)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField(default=0.0)),
                ('payment_type', models.CharField(blank=True, choices=[('SPOT_CASH', 'Spot Cash'), ('DOWNPAYMENT', 'Downpayment'), ('INSTALLMENT', 'Installment'), ('OTHERS', 'Others')], default='DOWNPAYMENT', max_length=256, null=True)),
                ('remarks', models.CharField(blank=True, max_length=256, null=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='memorial_park_mgmnt_app.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField(default=0.0)),
                ('service_type', models.CharField(blank=True, choices=[('CERTIFICATE_OF_OWNERSHIP', 'Certificate of Ownership'), ('CHANGE_OF_TITLE', 'Change of Title'), ('CHANGE_OF_LOT', 'Change of Lot'), ('INTERMENT', 'Interment'), ('OTHERS', 'Others')], default='INTERMENT', max_length=256, null=True)),
                ('remarks', models.CharField(blank=True, max_length=256, null=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='memorial_park_mgmnt_app.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='SpotOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(default=0.15)),
                ('contract', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spot_option', to='memorial_park_mgmnt_app.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='SpotPromo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(default=0.15)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.AddField(
            model_name='lot',
            name='lot_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memorial_park_mgmnt_app.LotType'),
        ),
        migrations.AddField(
            model_name='contract',
            name='lot',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lot_contract', to='memorial_park_mgmnt_app.Lot'),
        ),
        migrations.AddField(
            model_name='contract',
            name='referent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referral_contracts', to='memorial_park_mgmnt_app.Agent'),
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_agent_contracts', to='memorial_park_mgmnt_app.Agent'),
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_leader_contracts', to='memorial_park_mgmnt_app.Agent'),
        ),
        migrations.AddField(
            model_name='contract',
            name='unit_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_manager_contracts', to='memorial_park_mgmnt_app.Agent'),
        ),
        migrations.AddField(
            model_name='bill',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='memorial_park_mgmnt_app.Contract'),
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together={('contract', 'issue_date')},
        ),
    ]
