# Generated by Django 2.2.2 on 2020-05-24 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_app', '0003_auto_20200523_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='medicines',
            field=models.CharField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='symptoms',
            field=models.CharField(max_length=1500),
        ),
        migrations.DeleteModel(
            name='Medicines',
        ),
        migrations.DeleteModel(
            name='Symptoms',
        ),
    ]
