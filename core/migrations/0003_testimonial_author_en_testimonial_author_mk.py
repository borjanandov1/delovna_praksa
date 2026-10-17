from django.db import migrations, models


def backfill_author_mk(apps, schema_editor):
    Testimonial = apps.get_model('core', 'Testimonial')
    Testimonial.objects.filter(author_mk__isnull=True).update(
        author_mk=models.F('author')
    )


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_faq_answer_en_faq_answer_mk_faq_question_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='author_en',
            field=models.CharField(max_length=100, null=True, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='author_mk',
            field=models.CharField(max_length=100, null=True, verbose_name='author'),
        ),
        migrations.RunPython(backfill_author_mk, migrations.RunPython.noop),
    ]
