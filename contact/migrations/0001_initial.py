import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='phone')),
                ('subject', models.CharField(max_length=200, verbose_name='subject')),
                ('message', models.TextField(verbose_name='message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='received')),
                ('is_read', models.BooleanField(default=False, verbose_name='read')),
            ],
            options={
                'verbose_name': 'contact message',
                'verbose_name_plural': 'contact messages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(max_length=40, verbose_name='phone')),
                ('preferred_date', models.DateField(verbose_name='preferred date')),
                ('preferred_time', models.TimeField(blank=True, null=True, verbose_name='preferred time')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=12, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('gym_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='training.gymclass', verbose_name='class')),
            ],
            options={
                'verbose_name': 'booking',
                'verbose_name_plural': 'bookings',
                'ordering': ['-created_at'],
            },
        ),
    ]
