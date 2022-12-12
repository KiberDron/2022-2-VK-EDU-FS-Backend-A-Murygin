from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .serializers import UserSerializer


class GetUser(LoginRequiredMixin, generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(id=user_id)
