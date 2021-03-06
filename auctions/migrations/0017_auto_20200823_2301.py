# Generated by Django 3.0.8 on 2020-08-23 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200823_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidVal', models.IntegerField()),
                ('currentHighestBidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currentHighestBid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='currentBid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bidOn', to='auctions.Bid'),
        ),
    ]
