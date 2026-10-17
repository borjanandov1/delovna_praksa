from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_testimonial_author_en_testimonial_author_mk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='map_lat',
            field=models.FloatField(default=42.003, verbose_name='map latitude'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='map_lng',
            field=models.FloatField(default=21.4008, verbose_name='map longitude'),
        ),
    ]
