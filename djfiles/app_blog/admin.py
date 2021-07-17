from django.contrib import admin

from app_blog.models import Profile, Blog, FileHolder, Avatar


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'about_me', 'user')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'content',)


@admin.register(FileHolder)
class FileHolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at',)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'profile',)
