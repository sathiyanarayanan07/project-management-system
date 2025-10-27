from django.urls import path
from . import views   

urlpatterns = [
    path("register/",views.user_register,name="register"),
    path("user_login/",views.user_login,name="user_login")


]