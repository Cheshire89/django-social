from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
    # PasswordChangeView,
    # PasswordChangeDoneView,
    # PasswordResetView,
    # PasswordResetDoneView,
    # PasswordResetConfirmView,
    # PasswordResetCompleteView

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', view=LogoutView.as_view(), name='logout'),
    path('register/', views.user_register, name='register'),


    # path('password-change/', view=PasswordChangeView.as_view(), name='password_change'),
    # path('password-change/done/', view=PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password-reset/', view=PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done', view=PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', view=PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', view=PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', views.dashboard, name='dashboard'),
]