# Generated by Django 4.2.4 on 2024-01-14 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_product_color_productcolors'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='category',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
