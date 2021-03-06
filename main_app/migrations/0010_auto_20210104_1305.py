# Generated by Django 3.1.1 on 2021-01-04 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20201221_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdata',
            name='DOM',
            field=models.CharField(default='NA', max_length=10),
        ),
        migrations.CreateModel(
            name='CustomerOnboardData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeID', models.CharField(max_length=150)),
                ('total_amount', models.FloatField()),
                ('tierRuleNo', models.IntegerField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('customerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.customerdata')),
            ],
        ),
    ]
