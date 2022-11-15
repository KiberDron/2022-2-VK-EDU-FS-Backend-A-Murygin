from django.urls import path

from . import views

app_name = 'chats'
urlpatterns = [
    path('', views.ChatList.as_view(), name='chat_list'),
    path('create/', views.CreateChat.as_view(), name='create_chat'),
    path('<int:pk>/', views.GetUpdateDeleteChat.as_view(), name='get_update_delete_chat'),
    path('<int:chat_id>/messages/', views.ChatMessagesList.as_view(), name='chat_messages_list'),
    path('<int:chat_id>/messages/create/', views.CreateMessage.as_view(), name='create_message'),
    path('messages/<int:pk>/', views.GetUpdateDeleteMessage.as_view(), name='get_update_delete_message'),
    path('messages/<int:pk>/read/', views.MarkMessageAsRead.as_view(), name='mark_message_as_read'),
    path('<int:pk>/add/', views.AddUserToChat.as_view(), name='add_user_to_chat'),
    path('<int:pk>/delete/', views.DeleteUserFromChat.as_view(), name='delete_user_from_chat'),
]
