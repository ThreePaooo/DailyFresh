# Generated by Django 2.1.1 on 2018-10-09 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20181009_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 9, 17, 56, 25, 907833), verbose_name='订单创建时间'),
        ),
    ]
