# Generated by Django 2.2.16 on 2022-07-20 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0007_auto_20220720_1456'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name'], 'verbose_name': 'Произведения'},
        ),
    ]
