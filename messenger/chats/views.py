from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Chat, Message
# использовать postman для тестирования


@require_http_methods(['GET'])
def chat_list(request):
    chats = Chat.objects.all().values()
    return JsonResponse({"chats": list(chats)})


@require_http_methods(['GET'])
def chat_page(request, chat_id):
    chat = Chat.objects.filter(id=chat_id).values()[0]
    return JsonResponse({"chat": chat})  # +сообщения в чате


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
@require_http_methods(['POST'])  # DELETE
def delete_chat(request):
    data = request.POST
    chat_id = data.get('delete_chat_id')
    chat_to_delete = Chat.objects.get(id=chat_id)
    chat_to_delete_serializable = Chat.objects.filter(id=chat_id).values()[0]
    chat_to_delete.delete()
    return JsonResponse({"deleted chat": chat_to_delete_serializable})


@csrf_exempt
@require_http_methods(['POST'])  # PUT/PATCH
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
