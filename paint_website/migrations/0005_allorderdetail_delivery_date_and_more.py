# Generated by Django 5.0 on 2024-04-13 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paint_website', '0004_shoppingcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='allorderdetail',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='allorderdetail',
            name='delivery_id',
            field=models.CharField(default='pD4LA0wY3b', max_length=50),
        ),
    ]
