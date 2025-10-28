from django.urls import path
from .import views   

urlpatterns = [
    path("register/",views.user_register,name="register"),
    path("user_login/",views.user_login,name="user_login"),
    path("user_details/",views.user_details,name="user_details"),
    path("user_list/",views.user_list,name="user_list"),
    path("user_profile/<str:email>/",views.user_profile,name="user_profile"),
    path("user_profile_details/",views.user_profile_details,name="user_profile_details"),
    path("admin_login/",views.admin_login,name="admin_login"),
    path("create_Team/",views.create_Team,name="create_Team"),
    path("remove_team_member/",views.remove_team_member,name="remove_member"),
    path("update_team/",views.team_update,name="update_team"),
    #project
    path("create_project/",views.create_project,name="create_project"),
    path("project_delete/<str:name>/",views.project_delete,name="project_delete")


]