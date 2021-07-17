# Generated by Django 2.2 on 2021-03-16 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0005_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatar_profile', to='app_blog.Profile', verbose_name='профиль'),
        ),
    ]