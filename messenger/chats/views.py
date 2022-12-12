from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound, NotAcceptable
from .models import Chat, Message, ChatMember
from users.models import User
from .serializers import ChatSerializer, MessageSerializer, CreateMessageSerializer,\
    MessageReadStatusSerializer, UserInChatSerializer
from .permissions import IsMemberOrAdmin, IsMember, IsAuthor, IsAdmin
from .tasks import send_admin_email
from .utils import publish_message, clear_tags


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


@login_required
def home(request):
    response = redirect('http://127.0.0.1:3000/')
    return response


def login(request):
    return render(request, 'login.html')


class ChatList(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def get_queryset(self):
        chat_member_list = ChatMember.objects.filter(user_id=self.request.user.id).values()
        chat_id_list = [item['chat_id'] for item in chat_member_list]
        return Chat.objects.filter(pk__in=chat_id_list)


class CreateChat(LoginRequiredMixin, generics.CreateAPIView):
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        chat = serializer.save()
        ChatMember.objects.get_or_create(chat_id=chat.id, user_id=self.request.user.id, is_admin=True)
        return chat


class GetUpdateDeleteChat(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = (IsMemberOrAdmin,)

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        return Chat.objects.filter(id=chat_id)


class ChatMessagesList(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsMember,)

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat__id=chat_id)


class CreateMessage(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)
        author_id = self.request.data.get("author")
        get_object_or_404(ChatMember, chat_id=chat_id, user_id=author_id)
        text = clear_tags(self.request.data.get("text"))
        message_obj = Message.objects.create(chat_id=chat_id, author_id=author_id, text=text)
        message = Message.objects.filter(id=message_obj.id).values()[0]
        publish_message(message)
        return JsonResponse({})


class GetUpdateDeleteMessage(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        message_id = self.kwargs['pk']
        return Message.objects.filter(id=message_id)

    def perform_update(self, serializer):
        message_id = self.kwargs['pk']
        text = self.request.data.get("text")
        read_status = (self.request.data.get("read_status") == "true")
        return Message.objects.filter(id=message_id).update(text=text, read_status=read_status)


class MarkMessageAsRead(LoginRequiredMixin, generics.UpdateAPIView):
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


class AddUserToChat(LoginRequiredMixin, generics.CreateAPIView):
    serializer_class = UserInChatSerializer
    permission_classes = (IsAdmin,)

    def perform_create(self, serializer):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        chat_title = chat.title
        user_id = self.request.data.get("user")
        user = get_object_or_404(User, id=user_id)
        username = user.username
        ChatMember.objects.get_or_create(chat_id=chat_id, user_id=user_id)
        send_admin_email.delay(username, chat_title)
        return chat


class DeleteUserFromChat(LoginRequiredMixin, generics.DestroyAPIView):
    serializer_class = UserInChatSerializer
    permission_classes = (IsAdmin,)

    def destroy(self, request, *args, **kwargs):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, id=chat_id)
        member_id = self.kwargs["member_id"]
        chat_member = get_object_or_404(ChatMember, id=member_id)
        chat_member.delete()
        return JsonResponse({})
