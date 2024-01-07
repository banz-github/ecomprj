# Generated by Django 4.2.4 on 2024-01-07 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customorder_prototype2', '0016_remove_material_foam_percubicft_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='foam_percubicft_price',
            field=models.DecimalField(decimal_places=2, default=400, max_digits=10),
            preserve_default=False,
        ),
    ]
