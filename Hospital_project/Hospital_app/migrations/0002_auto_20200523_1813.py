# Generated by Django 2.2.2 on 2020-05-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='Degree',
            field=models.CharField(default='degree', max_length=1500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(default='specializtion', max_length=1500),
            preserve_default=False,
        ),
    ]