from django.urls import path
from . views import UserRegistrationView, UserLoginView, user_logout, UserProfileView, ProfileUpdateView, change_pass
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('edit_profile/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('change_pass/', change_pass, name='change_pass'),
    path('logout/', user_logout, name='logout'),
]
