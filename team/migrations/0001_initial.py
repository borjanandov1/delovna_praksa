from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('name_mk', models.CharField(max_length=80, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=80, null=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'specialty',
                'verbose_name_plural': 'specialties',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='full name')),
                ('slug', models.SlugField(max_length=140, unique=True, verbose_name='slug')),
                ('role', models.CharField(max_length=120, verbose_name='role')),
                ('role_mk', models.CharField(max_length=120, null=True, verbose_name='role')),
                ('role_en', models.CharField(max_length=120, null=True, verbose_name='role')),
                ('short_bio', models.CharField(blank=True, max_length=255, verbose_name='short bio')),
                ('short_bio_mk', models.CharField(blank=True, max_length=255, null=True, verbose_name='short bio')),
                ('short_bio_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='short bio')),
                ('bio', models.TextField(blank=True, verbose_name='biography')),
                ('bio_mk', models.TextField(blank=True, null=True, verbose_name='biography')),
                ('bio_en', models.TextField(blank=True, null=True, verbose_name='biography')),
                ('photo', models.ImageField(blank=True, upload_to='team/', verbose_name='photo')),
                ('certifications', models.TextField(blank=True, help_text='One per line.', verbose_name='certifications')),
                ('certifications_mk', models.TextField(blank=True, help_text='One per line.', null=True, verbose_name='certifications')),
                ('certifications_en', models.TextField(blank=True, help_text='One per line.', null=True, verbose_name='certifications')),
                ('years_experience', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='years of experience')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('specialties', models.ManyToManyField(blank=True, related_name='members', to='team.specialty', verbose_name='specialties')),
            ],
            options={
                'verbose_name': 'team member',
                'verbose_name_plural': 'team members',
                'ordering': ['order', 'name'],
            },
        ),
    ]
