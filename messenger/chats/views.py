import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Chat, Message
from users.models import User


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
    data = request.POST.dict()
    chat = Chat.objects.create(**data)
    chat_serializable = Chat.objects.filter(id=chat.id).values()[0]
    return JsonResponse({"chat created": chat_serializable}, status=201)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_chat(request, chat_id):
    data = get_object_or_404(Chat, id=chat_id)
    chat_to_delete_serializable = Chat.objects.filter(id=chat_id).values()[0]
    data.delete()
    return JsonResponse({"chat deleted": chat_to_delete_serializable})


@csrf_exempt
@require_http_methods(['PATCH'])
def modify_chat(request, chat_id):
    get_object_or_404(Chat, id=chat_id)
    data = json.loads(json.dumps(request.body.decode()))
    separated_data = data.replace('%20', ' ').split('&')
    res_data = {item.split('=')[0]: item.split('=')[1] for item in separated_data}
    Chat.objects.filter(id=chat_id).update(**res_data)
    modified_chat = Chat.objects.filter(id=chat_id).values()[0]
    return JsonResponse({"chat modified": modified_chat})


@require_http_methods(['GET'])
def chat_messages(request, chat_id):
    get_object_or_404(Chat, id=chat_id)
    messages_in_chat = Message.objects.filter(chat_id=chat_id).values()
    return JsonResponse({"chat messages": list(messages_in_chat)})


@csrf_exempt
@require_http_methods(['POST'])
def create_message(request):
    chat_id = request.POST.get("chat_id")
    author_id = request.POST.get("author_id")
    text = request.POST.get("message_text")
    user = get_object_or_404(User, id=author_id)
    chat = get_object_or_404(Chat, id=chat_id)
    if text and user.id in [item["id"] for item in chat.users.values()]:
        message = Message.objects.create(**request.POST.dict())
        message_serializable = Message.objects.filter(id=message.id).values()[0]
        return JsonResponse({"message created": message_serializable}, status=201)
    return JsonResponse({"message created": False}, status=400)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_message(request, message_id):
    data = get_object_or_404(Message, id=message_id)
    message_to_delete_serializable = Message.objects.filter(id=message_id).values()[0]
    data.delete()
    return JsonResponse({"message deleted": message_to_delete_serializable})


@csrf_exempt
@require_http_methods(['PATCH'])
def modify_message(request, message_id):
    get_object_or_404(Message, id=message_id)
    data = json.loads(json.dumps(request.body.decode()))
    separated_data = data.replace('%20', ' ').split('&')
    res_data = {item.split('=')[0]: item.split('=')[1] for item in separated_data}
    Message.objects.filter(id=message_id).update(**res_data)
    modified_message = Message.objects.filter(id=message_id).values()[0]
    return JsonResponse({"message modified": modified_message})


@csrf_exempt
@require_http_methods(['PATCH'])
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if not message.read_status:
        Message.objects.filter(id=message_id).update(read_status=True)
        return JsonResponse({"message marked as read": message_id})
    return JsonResponse({"message already read": f"id={message_id}"}, status=400)
