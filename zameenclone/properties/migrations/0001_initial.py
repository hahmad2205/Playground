# Generated by Django 5.0.6 on 2024-07-02 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_title', models.CharField(max_length=100)),
                ('property_header', models.CharField(max_length=100)),
                ('property_type', models.CharField(max_length=50)),
                ('property_price', models.PositiveIntegerField()),
                ('property_location', models.CharField(max_length=50)),
                ('number_of_bath', models.PositiveIntegerField()),
                ('number_of_bed', models.PositiveIntegerField()),
                ('property_area', models.CharField(max_length=50)),
                ('listing_purpose', models.CharField(max_length=50)),
                ('description_text', models.TextField()),
                ('whatsapp', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyOffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PropertyAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_amenity_key', models.CharField(max_length=50)),
                ('amenity_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_amenities', to='core.amenityoption')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_amenities', to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_link', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_images', to='properties.property')),
            ],
        ),
    ]
