# Generated by Django 3.0.7 on 2021-02-08 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_auto_20210208_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.BooleanField(),
        ),
    ]
