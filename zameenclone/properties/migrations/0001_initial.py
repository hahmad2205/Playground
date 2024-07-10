# Generated by Django 5.0.6 on 2024-07-10 10:33

import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('area', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('header', models.TextField()),
                ('location', models.TextField()),
                ('purpose', models.CharField(default='for sale', max_length=255)),
                ('number_of_bath', models.PositiveSmallIntegerField()),
                ('number_of_bed', models.PositiveSmallIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(default='house', max_length=255)),
                ('whatsapp_number', models.CharField(max_length=13)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.PositiveIntegerField(blank=True, null=True)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.amenityoption')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_amenities', to='properties.property')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='property',
            name='amenities',
            field=models.ManyToManyField(related_name='amenities', to='properties.propertyamenity'),
        ),
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('image_url', models.TextField()),
                ('image', models.FileField(upload_to='')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='properties.property')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyOffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('price', models.PositiveIntegerField()),
                ('offered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_offers', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='properties.property')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
