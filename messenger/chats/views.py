import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Chat, Message, ChatMember


@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'chats/homepage.html')


@require_http_methods(['GET'])
def chat_list(request):
    chats = Chat.objects.all().values()
    return JsonResponse({"chats": list(chats)})


@require_http_methods(['GET'])
def chat_page(request, chat_id):
    get_object_or_404(Chat, id=chat_id)
    chat = Chat.objects.filter(id=chat_id).values()[0]
    messages = Message.objects.filter(chat=chat_id).values()
    return JsonResponse({"chat": chat, "messages": list(messages)})


@csrf_exempt
@require_http_methods(['POST'])
def create_chat(request):
    data = json.loads(request.body)
    chat = Chat.objects.create(**data)
    return JsonResponse({"chat_pk": chat.id}, status=201)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_chat(request, chat_id):
    data = get_object_or_404(Chat, id=chat_id)
    data.delete()
    return JsonResponse({})


@csrf_exempt
@require_http_methods(['PATCH'])
def modify_chat(request, chat_id):
    get_object_or_404(Chat, id=chat_id)
    data = json.loads(request.body)
    Chat.objects.filter(id=chat_id).update(**data)
    return JsonResponse({"chat_pk": chat_id})


@require_http_methods(['GET'])
def chat_messages(request, chat_id):
    get_object_or_404(Chat, id=chat_id)
    messages_in_chat = Message.objects.filter(chat_id=chat_id).values()
    return JsonResponse({"messages": list(messages_in_chat)})


@csrf_exempt
@require_http_methods(['POST'])
def create_message(request):
    data = json.loads(request.body)
    chat_id = data["chat_id"]
    author_id = data["author_id"]
    text = data["message_text"]
    if text and get_object_or_404(ChatMember, chat_id=chat_id, user_id=author_id):
        message = Message.objects.create(**data)
        return JsonResponse({"message_pk": message.id}, status=201)
    return JsonResponse({"message_pk": False}, status=400)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_message(request, message_id):
    data = get_object_or_404(Message, id=message_id)
    data.delete()
    return JsonResponse({})


@csrf_exempt
@require_http_methods(['PATCH'])
def modify_message(request, message_id):
    get_object_or_404(Message, id=message_id)
    data = json.loads(request.body)
    Message.objects.filter(id=message_id).update(**data)
    return JsonResponse({"message_pk": message_id})


@csrf_exempt
@require_http_methods(['PATCH'])
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if not message.read_status:
        Message.objects.filter(id=message_id).update(read_status=True)
        return JsonResponse({"message_pk": message_id})
    return JsonResponse({"message_pk": False}, status=400)
