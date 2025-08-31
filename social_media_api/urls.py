"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# social_media_api/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views  # Import the authtoken views
from users.views import RegisterUserView  # Import your new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),
    path('followers/', include('followers.urls')),
    path('auth/register/', RegisterUserView.as_view(), name='register'), # New registration path
    path('auth/login/', views.obtain_auth_token, name='login'), # Built-in login path
]