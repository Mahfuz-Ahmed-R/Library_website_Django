from django.urls import path
from .views import UserAccountView, UserLoginView, UserLogout, UserProfileView, UserDetailsChange, PasswordChangeView
urlpatterns = [
    path('register/', UserAccountView.as_view(), name = 'register'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', UserLogout.as_view(), name = 'logout'),
    path('edit/', UserDetailsChange.as_view(), name = 'edit'),
    path('password/', PasswordChangeView.as_view(), name = 'password'),
]
