# Generated by Django 2.1.1 on 2018-10-10 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20181009_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 10, 9, 29, 48, 626249), verbose_name='订单创建时间'),
        ),
    ]
