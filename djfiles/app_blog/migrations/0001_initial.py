# Generated by Django 2.2 on 2021-03-14 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='заголовок')),
                ('content', models.TextField(max_length=500, verbose_name='контент')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('about_me', models.TextField(blank=True, max_length=1000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='FileHolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='files/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_file', to='app_blog.Blog', verbose_name='блог')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='files',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_blog', to='app_blog.FileHolder', verbose_name='файлы'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_blog', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
