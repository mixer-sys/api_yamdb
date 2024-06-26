# Generated by Django 3.2 on 2023-08-02 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_title_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('-name',), 'verbose_name': 'жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-year',), 'verbose_name': 'произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]
