from django.urls import path

from . import views

app_name = 'chats'
urlpatterns = [
    # path('', views.chat_list, name='chat_list'),
    path('', views.ChatList.as_view(), name='chat_list'),
    #path('<int:chat_id>/', views.chat_page, name='chat_page'),
    #path('create/', views.create_chat, name='create_chat'),
    path('create/', views.CreateChat.as_view(), name='create_chat'),
    #path('delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    #path('modify/<int:chat_id>/', views.modify_chat, name='modify_chat'),
    path('<int:pk>/', views.GetUpdateDeleteChat.as_view(), name='get_update_delete_chat'),
    #path('<int:chat_id>/messages/', views.chat_messages, name='chat_messages'),
    path('<int:chat_id>/messages/', views.ChatMessagesList.as_view(), name='chat_messages_list'),
    #path('messages/create/', views.create_message, name='create_message'),
    path('messages/create/', views.CreateMessage.as_view(), name='create_message'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/modify/<int:message_id>/', views.modify_message, name='modify_message'),
    path('messages/mark_as_read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read')
]
