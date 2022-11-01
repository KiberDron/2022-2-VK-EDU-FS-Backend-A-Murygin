from django.urls import path

from . import views

app_name = 'chats'
urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_page, name='chat_page'),
    path('create/', views.create_chat, name='create_chat'),
    path('delete/', views.delete_chat, name='delete_chat'),
    path('modify/', views.modify_chat, name='modify_chat')
]
