# Generated by Django 4.2.7 on 2023-12-08 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('set_is_active', 'Может блокировать пользователя')]},
        ),
    ]
