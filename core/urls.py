from django.urls import path

from django.contrib.auth import views as auth_views

from .views import CustomPasswordResetView

from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset URLs
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    #path('password-reset/', auth_views.PasswordResetView.as_view(template_name='forget_password/password_reset_form.html'), name='password-reset'),
    path('passwor-reset/email-sent/', auth_views.PasswordResetDoneView.as_view(template_name='forget_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='forget_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='forget_password/password_reset_complete.html'), name='password_reset_complete'),

]