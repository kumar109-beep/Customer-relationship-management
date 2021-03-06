# Generated by Django 2.2.10 on 2021-08-29 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_supervisor_amountofpurchase_report_history_supervisor_noofvisit_report_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='supervisor_Report_History_for_visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportID', models.CharField(max_length=50, unique=True)),
                ('selected_stores', models.TextField()),
                ('dateRange', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('supervisor_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.supervisorDetails')),
            ],
        ),
        migrations.CreateModel(
            name='supervisor_Report_History_for_amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportID', models.CharField(max_length=50, unique=True)),
                ('selected_stores', models.TextField()),
                ('dateRange', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('supervisor_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.supervisorDetails')),
            ],
        ),
    ]
