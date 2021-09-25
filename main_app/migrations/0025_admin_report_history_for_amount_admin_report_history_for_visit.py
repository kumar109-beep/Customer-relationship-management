# Generated by Django 2.2.10 on 2021-08-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_supervisor_report_history_for_amount_supervisor_report_history_for_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_Report_History_for_amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportID', models.CharField(max_length=50, unique=True)),
                ('selected_stores', models.TextField()),
                ('dateRange', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='admin_Report_History_for_visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportID', models.CharField(max_length=50, unique=True)),
                ('selected_stores', models.TextField()),
                ('dateRange', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
