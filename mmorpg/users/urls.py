from django.urls import path
from allauth.account.views import LoginView, LogoutView
from .views import CustomSignupView, verify_email, resend_code, ProfilePage

urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'), 
    path('verify-email/', verify_email, name='verify_email'),
    path('resend-code/', resend_code, name='resend_code'),
    path('profile/', ProfilePage.as_view(), name='profile'),
]
