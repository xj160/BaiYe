# Generated by Django 3.0.3 on 2020-04-12 10:56

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='icon',
            field=models.ImageField(blank=True, storage=system.storage.ImageStorage(), upload_to='up_load/'),
        ),
    ]
