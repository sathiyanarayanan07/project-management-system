from django.urls import path
from . import views   

urlpatterns = [
    path("register/",views.user_register,name="register"),
    path("user_login/",views.user_login,name="user_login"),
    path("user_details/",views.user_details,name="user_details"),
    path("user_profile/<str:email>/",views.user_profile,name="user_profile"),
    path("user_profile_details/",views.user_profile_details,name="user_profile_details")


]