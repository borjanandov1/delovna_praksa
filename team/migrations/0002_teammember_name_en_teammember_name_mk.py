from django.db import migrations, models


def backfill_name_mk(apps, schema_editor):
    TeamMember = apps.get_model('team', 'TeamMember')
    TeamMember.objects.filter(name_mk__isnull=True).update(name_mk=models.F('name'))


class Migration(migrations.Migration):
    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='name_en',
            field=models.CharField(max_length=120, null=True, verbose_name='full name'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='name_mk',
            field=models.CharField(max_length=120, null=True, verbose_name='full name'),
        ),
        migrations.RunPython(backfill_name_mk, migrations.RunPython.noop),
    ]
