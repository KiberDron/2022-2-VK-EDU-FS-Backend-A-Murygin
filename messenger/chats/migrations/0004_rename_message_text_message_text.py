# Generated by Django 4.1.2 on 2022-11-25 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_alter_message_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message_text',
            new_name='text',
        ),
    ]
