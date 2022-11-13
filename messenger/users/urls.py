from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('<int:user_id>/', views.user_info, name='user_info'),
    path('add/', views.add_user_to_chat, name='add_user_to_chat'),
    path('delete/', views.delete_user_from_chat, name='delete_user_from_chat')
]
