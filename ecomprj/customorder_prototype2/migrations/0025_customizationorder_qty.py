# Generated by Django 4.2.4 on 2024-01-09 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customorder_prototype2', '0024_customizationorder_receipt_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customizationorder',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
