# Generated by Django 3.1.1 on 2020-12-17 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_schedulelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulelist',
            name='emailList',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='schedulelist',
            name='emailSubject',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='schedulelist',
            name='emailText',
            field=models.TextField(default='NA'),
        ),
    ]