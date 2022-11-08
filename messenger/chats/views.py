from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Chat, Message


@require_http_methods(['GET'])
def chat_list(request):
    chats = Chat.objects.all().values()
    return JsonResponse({"chats": list(chats)})


@require_http_methods(['GET'])
def chat_page(request, chat_id):
    chat = Chat.objects.filter(id=chat_id).values()[0]
    messages = Message.objects.filter(chat=chat_id).values()
    return JsonResponse({"chat": chat, "messages": list(messages)})


@csrf_exempt
@require_http_methods(['POST'])
def create_chat(request):
    data = request.POST
    title = data.get('title')
    new_chat = Chat(title=title)
    new_chat.save()
    new_chat_id = new_chat.id
    new_chat_serializable = Chat.objects.filter(id=new_chat_id).values()[0]
    return JsonResponse({"chat": new_chat_serializable}, status=201)


@csrf_exempt
@require_http_methods(['DELETE', 'GET'])
def delete_chat(request, chat_id):
    data = get_object_or_404(Chat, id=chat_id)
    chat_to_delete_serializable = Chat.objects.filter(id=chat_id).values()[0]
    data.delete()
    return JsonResponse({"deleted chat": chat_to_delete_serializable})


@csrf_exempt
@require_http_methods(['POST'])
def modify_chat(request):
    data = request.POST
    chat_id = data.get('modify_chat_id')
    new_title = data.get('new_title')
    Chat.objects.filter(id=chat_id).update(title=new_title)
    modified_chat = Chat.objects.filter(id=chat_id).values()[0]
    return JsonResponse({"chat modified": modified_chat})


@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'chats/homepage.html')
