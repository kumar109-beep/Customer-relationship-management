# Generated by Django 2.2.10 on 2021-06-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_auto_20210120_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdata',
            name='emailSubscription',
            field=models.CharField(default='True', max_length=6),
        ),
    ]