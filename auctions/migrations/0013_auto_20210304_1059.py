# Generated by Django 3.1.5 on 2021-03-04 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210303_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date',
            field=models.CharField(default='123', max_length=64),
        ),
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.CharField(default='123', max_length=64),
        ),
    ]