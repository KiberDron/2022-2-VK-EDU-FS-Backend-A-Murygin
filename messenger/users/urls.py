from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('<int:pk>/', views.GetUser.as_view(), name='get_user'),
]
