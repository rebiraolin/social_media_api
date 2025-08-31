# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, UserViewSet, UserProfileView
from .views_html import register_view, profile_view, login_view, logout_view, edit_profile_view, remove_profile_picture

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    # -----------------------
    # API URLs
    # -----------------------
    path('api/register/', RegisterUserView.as_view(), name='user-register-api'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile-api'),
    path('api/', include(router.urls)),

    # -----------------------
    # HTML pages
    # -----------------------
    path('register/', register_view, name='user-register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='my-profile'),  # Changed URL name to 'my-profile'
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/remove-picture/', remove_profile_picture, name='remove_profile_picture'),
    path('profile/<str:username>/', profile_view, name='user-profile'), # This one is for other users
]