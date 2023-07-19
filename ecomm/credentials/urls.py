from django.urls import path
from . import views

app_name = 'credentials'

urlpatterns = [
    path('', views.register_login, name='login_register'),
    path('logout/', views.user_logout, name='logout'),
 ]
