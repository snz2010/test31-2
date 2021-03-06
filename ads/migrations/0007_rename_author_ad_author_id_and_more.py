# Generated by Django 4.0.5 on 2022-06-15 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_remove_ad_author_id_alter_ad_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='author',
            new_name='author_id',
        ),
        migrations.RenameField(
            model_name='ad',
            old_name='category',
            new_name='category_id',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='address',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='status',
        ),
        migrations.AlterField(
            model_name='ad',
            name='is_published',
            field=models.CharField(choices=[('true', 'опубликовано'), ('false', 'не опубликовано')], default='false', max_length=5),
        ),
    ]
