import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import User
from chats.models import Chat


@require_http_methods(['GET'])
def user_info(request, user_id):
    get_object_or_404(User, id=user_id)
    user = User.objects.filter(id=user_id).values()[0]
    return JsonResponse({"user info": user})


@csrf_exempt
@require_http_methods(['POST'])
def add_user_to_chat(request):
    user_id = request.POST.get("user_id")
    chat_id = request.POST.get("chat_id")
    user = get_object_or_404(User, id=user_id)
    chat = get_object_or_404(Chat, id=chat_id)
    if user_id not in [item["id"] for item in chat.users.values()]:
        chat.users.add(user)
        return JsonResponse({"info": f"user with id={user_id} added to chat with id={chat_id}"})
    return JsonResponse({"info": f"user with id={user_id} is already in chat with id={chat_id}"}, status=400)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_user_from_chat(request):
    data = json.loads(json.dumps(request.body.decode()))
    separated_data = data.replace('%20', ' ').split('&')
    res_data = {item.split('=')[0]: item.split('=')[1] for item in separated_data}
    user_id = res_data.get("user_id")
    chat_id = res_data.get("chat_id")
    user = get_object_or_404(User, id=user_id)
    chat = get_object_or_404(Chat, id=chat_id)
    if int(user_id) in [item["id"] for item in chat.users.values()]:
        chat.users.remove(user)
        return JsonResponse({"info": f"user with id={user_id} deleted from chat with id={chat_id}"})
    return JsonResponse({"info": f"user with id={user_id} is not a member of chat with id={chat_id}"}, status=400)
