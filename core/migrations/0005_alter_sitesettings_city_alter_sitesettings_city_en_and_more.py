from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_sitesettings_map_lat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='city',
            field=models.CharField(blank=True, max_length=80, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='city_en',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='city_mk',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='city'),
        ),
    ]
