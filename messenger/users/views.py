from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render


class GetUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(id=user_id)
