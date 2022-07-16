# Generated by Django 4.0.3 on 2022-04-04 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_prettynumber_level_alter_prettynumber_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prettynumber',
            name='level',
            field=models.SmallIntegerField(choices=[(1, '青铜'), (2, '白银'), (3, '黄金'), (4, '钻石'), (5, '王者')], default=2, verbose_name='级别'),
        ),
        migrations.AlterField(
            model_name='prettynumber',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '已占用'), (2, '未占用')], default=1, verbose_name='状态'),
        ),
    ]
