# Generated by Django 2.1.1 on 2018-09-29 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('abstract', models.CharField(blank=True, max_length=200, null=True, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='商品价格')),
                ('unit', models.CharField(max_length=20, verbose_name='售卖单位')),
                ('stock', models.IntegerField(default=0, verbose_name='商品库存')),
                ('desc', models.TextField(null=True, verbose_name='详细介绍')),
            ],
            options={
                'verbose_name': '商品信息管理',
                'verbose_name_plural': '商品信息管理',
                'db_table': 'goods',
            },
        ),
    ]