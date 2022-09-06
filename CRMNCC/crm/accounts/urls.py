from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'


urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/eit/', views.profile_edit, name='profile_edit'),
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('reset/', views.reset, name='reset'),
    ]
