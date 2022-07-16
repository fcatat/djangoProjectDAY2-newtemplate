# Generated by Django 3.2.13 on 2022-06-14 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0015_auto_20220613_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetsinfo',
            name='app',
            field=models.ManyToManyField(blank=True, null=True, to='app01.Application'),
        ),
        migrations.AlterField(
            model_name='assetsinfo',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.userinfo'),
        ),
    ]
