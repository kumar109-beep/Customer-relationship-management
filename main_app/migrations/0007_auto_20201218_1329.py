# Generated by Django 3.1.1 on 2020-12-18 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_store_manager_statusflag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store_manager',
            name='statusflag',
        ),
        migrations.AddField(
            model_name='store_detail',
            name='statusflag',
            field=models.BooleanField(default=1),
        ),
    ]
