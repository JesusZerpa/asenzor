# Generated by Django 3.1.4 on 2021-01-21 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asenzor', '0008_auto_20210109_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermeta',
            name='unique',
            field=models.BooleanField(default=False),
        ),
    ]
