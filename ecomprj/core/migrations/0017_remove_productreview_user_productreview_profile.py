# Generated by Django 4.2.4 on 2023-12-06 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0007_rename_full_name_profile_first_name_profile_active_and_more'),
        ('core', '0016_remove_address_user_address_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='user',
        ),
        migrations.AddField(
            model_name='productreview',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userauths.profile'),
        ),
    ]
