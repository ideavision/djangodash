from django.urls import path
from .views import login_view, register_user, profile_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', profile_view, name="profile"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password-reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password-reset-done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password-reset-confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password-reset-complete.html'
         ),
         name='password_reset_complete'),
]