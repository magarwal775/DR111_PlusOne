# Generated by Django 3.0.4 on 2020-08-02 18:51

from django.db import migrations
import mapbox_location_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=mapbox_location_field.models.LocationField(default=[73.8278, 15.4909], map_attrs={'center': [73.8278, 15.4909]}),
            preserve_default=False,
        ),
    ]
