from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipplan',
            name='period',
            field=models.CharField(max_length=40, verbose_name='period'),
        ),
        migrations.AlterField(
            model_name='membershipplan',
            name='period_en',
            field=models.CharField(max_length=40, null=True, verbose_name='period'),
        ),
        migrations.AlterField(
            model_name='membershipplan',
            name='period_mk',
            field=models.CharField(max_length=40, null=True, verbose_name='period'),
        ),
    ]
