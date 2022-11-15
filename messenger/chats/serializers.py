from rest_framework import serializers
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, chat):
        names = chat.users.values_list('username')
        single_names = [name[0] for name in names]
        return single_names

    class Meta:
        model = Chat
        fields = ['id', 'title', 'description', 'users']


class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'description', 'users']


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_chat(self, message):
        title = message.chat
        return str(title)

    def get_author(self, message):
        name = message.author
        return str(name)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'message_text', 'creation_date', 'read_status']


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'message_text', 'creation_date', 'read_status']
