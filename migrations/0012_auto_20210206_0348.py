# Generated by Django 3.1.4 on 2021-02-06 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asenzor', '0011_auto_20210206_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='guid',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
