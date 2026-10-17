import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('name_mk', models.CharField(max_length=80, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=80, null=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'verbose_name': 'blog category',
                'verbose_name_plural': 'blog categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('title_mk', models.CharField(max_length=200, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=200, null=True, verbose_name='title')),
                ('slug', models.SlugField(max_length=220, unique=True, verbose_name='slug')),
                ('excerpt', models.TextField(max_length=400, verbose_name='excerpt')),
                ('excerpt_mk', models.TextField(max_length=400, null=True, verbose_name='excerpt')),
                ('excerpt_en', models.TextField(max_length=400, null=True, verbose_name='excerpt')),
                ('body', models.TextField(verbose_name='body')),
                ('body_mk', models.TextField(null=True, verbose_name='body')),
                ('body_en', models.TextField(null=True, verbose_name='body')),
                ('cover_image', models.ImageField(blank=True, upload_to='blog/', verbose_name='cover image')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='published at')),
                ('is_published', models.BooleanField(default=True, verbose_name='published')),
                ('views', models.PositiveIntegerField(default=0, editable=False, verbose_name='views')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='team.teammember', verbose_name='author')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-published_at'],
                'indexes': [models.Index(fields=['-published_at'], name='blog_post_publish_2c9212_idx')],
            },
        ),
    ]
