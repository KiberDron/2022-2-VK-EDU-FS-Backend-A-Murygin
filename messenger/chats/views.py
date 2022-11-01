from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


chats = [
        {'id': 1, 'title': 'Bob'},
        {'id': 2, 'title': 'Mark'},
        {'id': 3, 'title': 'Jennifer'}
    ]


@require_http_methods(['GET'])
def chat_list(request):
    return JsonResponse({'chats': chats})


@require_http_methods(['GET'])
def chat_page(request, chat_id):
    return JsonResponse(chats[chat_id - 1])


@csrf_exempt
@require_http_methods(['POST'])
def create_chat(request):
    data = request.POST
    title = data.get('title')
    new_id = len(chats) + 1
    chats.append({'id': new_id, 'title': title})
    return JsonResponse(chats[new_id - 1], status=201)


@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'chats/homepage.html')
