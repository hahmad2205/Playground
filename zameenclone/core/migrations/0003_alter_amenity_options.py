# Generated by Django 5.0.6 on 2024-07-30 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_amenity_options_alter_amenityoption_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name': 'Property amenity type', 'verbose_name_plural': 'Property amenity types'},
        ),
    ]
