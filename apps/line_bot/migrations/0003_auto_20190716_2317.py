# Generated by Django 2.2.3 on 2019-07-16 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0002_auto_20190716_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controllermodel',
            name='mod',
            field=models.IntegerField(choices=[(0, None), (1, 'rank'), (2, 'keyword')], null=True, verbose_name='Mod'),
        ),
    ]
