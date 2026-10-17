from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='answer_en',
            field=models.TextField(null=True, verbose_name='answer'),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_mk',
            field=models.TextField(null=True, verbose_name='answer'),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_en',
            field=models.CharField(max_length=255, null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_mk',
            field=models.CharField(max_length=255, null=True, verbose_name='question'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='city_en',
            field=models.CharField(default='Скопје', max_length=80, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='city_mk',
            field=models.CharField(default='Скопје', max_length=80, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='short_about_en',
            field=models.TextField(blank=True, null=True, verbose_name='short about'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='short_about_mk',
            field=models.TextField(blank=True, null=True, verbose_name='short about'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='street_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='street'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='street_mk',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='street'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='tagline_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='tagline'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='tagline_mk',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='tagline'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='role_en',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='role'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='role_mk',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='role'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='text_en',
            field=models.TextField(null=True, verbose_name='text'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='text_mk',
            field=models.TextField(null=True, verbose_name='text'),
        ),
    ]
