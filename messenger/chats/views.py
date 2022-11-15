from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import NotFound, NotAcceptable
from .models import Chat, Message
from users.models import User
from .serializers import ChatSerializer, CreateChatSerializer, MessageSerializer, CreateMessageSerializer,\
    MessageReadStatusSerializer, UserInChatSerializer


def redirect_view(request):
    response = redirect('/chats/')
    return response


class ChatList(generics.ListAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class CreateChat(generics.CreateAPIView):
    serializer_class = CreateChatSerializer


class GetUpdateDeleteChat(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        return Chat.objects.filter(id=chat_id)


class ChatMessagesList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat__id=chat_id)


class CreateMessage(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)
        author_id = self.request.data.get("author")
        author = get_object_or_404(User, id=author_id)
        if author.id in [item["id"] for item in chat.users.values()]:
            return serializer.save(chat=chat)
        else:
            raise NotFound(detail=f"User with id={author_id} is not in chat with id={chat_id}")


class GetUpdateDeleteMessage(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        message_id = self.kwargs['pk']
        return Message.objects.filter(id=message_id)


class MarkMessageAsRead(generics.UpdateAPIView):
    serializer_class = MessageReadStatusSerializer

    def get_queryset(self):
        message_id = self.kwargs['pk']
        return Message.objects.filter(id=message_id)

    def perform_update(self, serializer):
        message_id = self.kwargs['pk']
        message = get_object_or_404(Message, id=message_id)
        if not message.read_status:
            return Message.objects.filter(id=message_id).update(read_status=True)
        else:
            raise NotAcceptable(detail=f"Message with id={message_id} is already read")


class AddUserToChat(generics.RetrieveUpdateAPIView):
    serializer_class = UserInChatSerializer

    def get_queryset(self):
        chat_id = self.kwargs["pk"]
        return Chat.objects.filter(id=chat_id)

    def perform_update(self, serializer):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        users_id = self.request.data.get("users")
        for user_id in users_id:
            user = get_object_or_404(User, id=user_id)
            if user.id not in [item["id"] for item in chat.users.values()]:
                chat.users.add(user)
            else:
                continue
        return chat


class DeleteUserFromChat(generics.RetrieveUpdateAPIView):
    serializer_class = UserInChatSerializer

    def get_queryset(self):
        chat_id = self.kwargs["pk"]
        return Chat.objects.filter(id=chat_id)

    def perform_update(self, serializer):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        users_id = self.request.data.get("users")
        for user_id in users_id:
            user = get_object_or_404(User, id=user_id)
            if user.id in [item["id"] for item in chat.users.values()]:
                chat.users.remove(user)
            else:
                continue
        return chat
