# Generated by Django 2.2 on 2021-03-18 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0009_auto_20210317_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(help_text='Имя', max_length=20),
        ),
    ]
