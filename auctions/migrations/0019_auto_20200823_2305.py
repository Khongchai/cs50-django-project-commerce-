# Generated by Django 3.0.8 on 2020-08-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20200823_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='currentBid',
            field=models.IntegerField(default=1),
        ),
    ]