from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer
from .models import Profile
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile
