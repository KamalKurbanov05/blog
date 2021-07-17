# Generated by Django 2.2 on 2021-03-16 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0004_auto_20210315_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='avatar_profile/')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar_profile', to='app_blog.Profile', verbose_name='профиль')),
            ],
        ),
    ]