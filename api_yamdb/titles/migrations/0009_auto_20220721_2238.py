# Generated by Django 2.2.16 on 2022-07-21 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0008_auto_20220720_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]