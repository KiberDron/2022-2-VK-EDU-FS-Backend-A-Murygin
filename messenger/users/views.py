import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import User
from chats.models import Chat, ChatMember


@require_http_methods(['GET'])
def user_info(request, user_id):
    get_object_or_404(User, id=user_id)
    user = User.objects.filter(id=user_id).values()[0]
    return JsonResponse({"user": user})


@csrf_exempt
@require_http_methods(['POST'])
def add_user_to_chat(request):
    data = json.loads(request.body)
    user_id = data["user_id"]
    chat_id = data["chat_id"]
    get_object_or_404(User, id=user_id)
    get_object_or_404(Chat, id=chat_id)
    chat_members = ChatMember.objects.filter(chat_id=chat_id)
    if user_id not in [item["user_id"] for item in chat_members.values()]:
        ChatMember.objects.create(chat_id=chat_id, user_id=user_id)
        return JsonResponse({"info": f"user with id={user_id} added to chat with id={chat_id}"})
    return JsonResponse({"info": f"user with id={user_id} is already in chat with id={chat_id}"}, status=400)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_user_from_chat(request):
    data = json.loads(request.body)
    user_id = data["user_id"]
    chat_id = data["chat_id"]
    get_object_or_404(User, id=user_id)
    get_object_or_404(Chat, id=chat_id)
    chat_member = get_object_or_404(ChatMember, chat_id=chat_id, user_id=user_id)
    chat_member.delete()
    return JsonResponse({})

