# Generated by Django 3.0.7 on 2021-02-15 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_auto_20210208_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='status_code',
            field=models.IntegerField(default=1337),
            preserve_default=False,
        ),
    ]
