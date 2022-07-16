# Generated by Django 4.0.3 on 2022-04-04 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_alter_userinfo_create_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, verbose_name='号码')),
                ('price', models.IntegerField(default=0, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(1, '青铜'), (1, '白银'), (1, '黄金'), (1, '钻石'), (1, '王者')], verbose_name='级别')),
                ('status', models.SmallIntegerField(choices=[(1, '已占用'), (1, '未占用')], verbose_name='状态')),
            ],
        ),
    ]
