# Generated by Django 2.2 on 2021-03-17 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0008_auto_20210316_2057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='avatar',
            options={'verbose_name': 'Аватар', 'verbose_name_plural': 'Аватарки'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_blog', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
