# Generated by Django 3.2 on 2023-07-30 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Описание произведения'),
        ),
    ]
