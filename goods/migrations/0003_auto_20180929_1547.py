# Generated by Django 2.1.1 on 2018-09-29 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180929_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorymodel',
            options={'verbose_name': '商品分类管理', 'verbose_name_plural': '商品分类管理'},
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='number',
            field=models.IntegerField(default=0, verbose_name='排序字段'),
        ),
    ]