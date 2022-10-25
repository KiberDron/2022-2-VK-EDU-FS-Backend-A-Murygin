from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@require_http_methods(['GET'])
def chat_list(request):
    chats = [
        {'id': 1, 'title': 'Bob'},
        {'id': 2, 'title': 'Mark'},
        {'id': 3, 'title': 'Jennifer'}
    ]
    return JsonResponse({'chats': chats})


@require_http_methods(['GET'])
def chat_page(request, chat_id):
    return JsonResponse({'chat': chat_id})


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def create_chat(request, pk):
    return JsonResponse({'chat_pk': pk})


@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'chats/homepage.html')
