# Generated by Django 4.2.4 on 2023-10-25 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customorder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='base_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
