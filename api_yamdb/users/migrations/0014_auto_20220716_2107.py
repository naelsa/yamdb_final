# Generated by Django 2.2.16 on 2022-07-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20220716_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True, verbose_name='Электронная почта'),
            preserve_default=False,
        ),
    ]