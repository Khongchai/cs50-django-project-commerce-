# Generated by Django 3.0.8 on 2020-08-22 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200820_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='watchlistItem', to='auctions.Listing'),
        ),
    ]
