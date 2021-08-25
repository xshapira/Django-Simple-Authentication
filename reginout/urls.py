from django.urls import path,include
from .views import *
from django.contrib.auth.views import LogoutView, PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView, PasswordChangeDoneView
from django.conf import settings
from . import views

urlpatterns = [
    path('', HomeViewFBV, name="home"),

    path('posts/', PostListView.as_view(), name="posts"),
    
    path('login/', login_view, name="login"),
    
    path('register/', register_view, name="register"),
    
    path('resend-mail/', resendemail, name="resend"),
    
    path('password-change/', PasswordChange.as_view(), name="password_change"),

    path('password-change-done/', PasswordDone.as_view(), name="password_change_done"),
    
    path('logout/', LogoutView.as_view(next_page = settings.LOGOUT_REDIRECT_URL), name="logout"),
    
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('reset_password/', PasswordResetView.as_view(),name="password_reset"),
    
    path('reset_password_sent/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset_password_complete/', PasswordResetCompleteView.as_view(),name="password_reset_complete"),

]
