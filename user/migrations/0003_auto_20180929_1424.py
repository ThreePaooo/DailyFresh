# Generated by Django 2.1.1 on 2018-09-29 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180929_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectGoodsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=30, verbose_name='收货人')),
                ('detail_address', models.CharField(max_length=200, verbose_name='详细地址')),
                ('post_code', models.IntegerField(default=0, verbose_name='邮政编码')),
                ('tel', models.CharField(max_length=20, verbose_name='联系方式')),
                ('is_used', models.BooleanField(verbose_name='是否正在使用')),
            ],
            options={
                'verbose_name': '收货信息管理',
                'verbose_name_plural': '收货信息管理',
            },
        ),
        migrations.AlterModelOptions(
            name='usermodel',
            options={'verbose_name': '用户信息管理', 'verbose_name_plural': '用户信息管理'},
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='电子邮箱'),
        ),
        migrations.AddField(
            model_name='collectgoodsmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserModel'),
        ),
    ]
