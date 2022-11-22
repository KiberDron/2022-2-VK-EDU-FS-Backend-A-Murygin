from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound, NotAcceptable
from .models import Chat, Message, ChatMember
from users.models import User
from .serializers import ChatSerializer, MessageSerializer, CreateMessageSerializer,\
    MessageReadStatusSerializer, UserInChatSerializer


def redirect_view(request):
    response = redirect('/chats/')
    return response


class ChatList(generics.ListAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class CreateChat(generics.CreateAPIView):
    serializer_class = ChatSerializer


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
        raise NotAcceptable(detail=f"Message with id={message_id} is already read")


class AddUserToChat(generics.CreateAPIView):
    serializer_class = UserInChatSerializer

    def perform_create(self, serializer):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        user_id = self.request.data.get("user")
        user = get_object_or_404(User, id=user_id)
        ChatMember.objects.get_or_create(chat_id=chat_id, user_id=user_id)
        return chat


class DeleteUserFromChat(generics.DestroyAPIView):
    serializer_class = UserInChatSerializer

    def destroy(self, request, *args, **kwargs):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        member_id = self.kwargs["member_id"]
        chat_member = get_object_or_404(ChatMember, id=member_id)
        chat_member.delete()
        return JsonResponse({})
