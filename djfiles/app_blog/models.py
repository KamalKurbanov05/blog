from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# регистрация и аутентификация пользователей

class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile',
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=20, help_text='Имя')
    about_me = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Avatar(models.Model):
    profile = models.OneToOneField(
        Profile,
        related_name='avatar_profile',
        verbose_name='профиль',
        on_delete=models.CASCADE,
    )
    image = models.FileField(upload_to='avatar_profile/', null=True, )

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватарки'


class Blog(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_blog',
        verbose_name='пользователь',
        on_delete=models.SET_NULL, null=True,
    )
    title = models.CharField('заголовок', max_length=50, blank=True, null=True)
    content = models.TextField('контент', max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now=True, )
    published = models.DateTimeField('дата публикции', null=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class FileHolder(models.Model):
    blog = models.ForeignKey(
        Blog,
        related_name='blog_file',
        verbose_name='блог',
        on_delete=models.CASCADE,
    )
    image = models.FileField(upload_to='files/', null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
