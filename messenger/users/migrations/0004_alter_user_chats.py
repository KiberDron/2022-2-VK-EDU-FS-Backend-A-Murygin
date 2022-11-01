# Generated by Django 4.1.2 on 2022-11-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_message_author_alter_message_chat'),
        ('users', '0003_alter_user_options_user_birthday_user_chats_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chats',
            field=models.ManyToManyField(related_name='users', to='chats.chat', verbose_name='Чаты пользователя'),
        ),
    ]
