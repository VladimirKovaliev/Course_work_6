# Generated by Django 4.2.7 on 2024-01-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200, verbose_name='заголовок'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='количетсво просмотров'),
        ),
    ]
