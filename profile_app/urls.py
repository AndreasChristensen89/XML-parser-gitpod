from django.urls import path
from . import views

app_name = 'profile_app'

urlpatterns = [
    path('', views.profile, name='profiles'),
    path('update-user/', views.UpdateUser.as_view(), name="update_user"),
    path('<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('password/', views.PasswordChangeView.as_view(), name='password'),
]