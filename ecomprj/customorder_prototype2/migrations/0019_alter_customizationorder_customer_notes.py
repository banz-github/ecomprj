# Generated by Django 4.2.4 on 2024-01-08 16:47

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customorder_prototype2', '0018_foamtype_remove_material_foam_percubicft_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customizationorder',
            name='customer_notes',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True),
        ),
    ]
