from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
]
