# Generated by Django 2.2.16 on 2022-07-15 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20220715_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='Код для авторизации'),
        ),
    ]
