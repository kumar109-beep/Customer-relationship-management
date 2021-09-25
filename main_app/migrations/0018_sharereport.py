# Generated by Django 2.2.10 on 2021-08-09 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_groupreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='shareReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supervisor_email', models.CharField(max_length=50, unique=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('reportFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.groupReport')),
                ('supervisorFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.supervisorDetails')),
            ],
        ),
    ]
