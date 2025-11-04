from django.urls import path
from .import views   

urlpatterns = [
    path("register/",views.user_register,name="register"),
    path("user_login/",views.user_login,name="user_login"),
    path("user_details/",views.user_details,name="user_details"),
    path("user_list/",views.user_list,name="user_list"),
    path("user_delete/<str:email>/",views.user_delete,name="user_delete"),
    path("user_profile/<str:email>/",views.user_update,name="user_profile"),
    path("user_profile_details/",views.user_profile_details,name="user_profile_details"),
    path("admin_login/",views.admin_login,name="admin_login"),
    #team
    path("create_Team/",views.create_Team,name="create_Team"),
    path("remove_team_member/",views.remove_team_member,name="remove_member"),
    path("update_team/",views.team_update,name="update_team"),
    path("team_list/",views.team_list,name="team_list"),
    path("get_team_details/",views.get_team_details,name="get_team_details"),
    path("team_delete/<str:name>/",views.team_delete,name="team_delete"),
    #project
    path("create_project/",views.create_project,name="create_project"),
    path("project_list/",views.project_list,name="project_list"),
    path("get_project_details/",views.get_project_details,name="get_project_details"),
    path("project_delete/<str:name>/",views.project_delete,name="project_delete"),
    path("project_update/<str:project_name>/",views.project_update,name="project_update"),
    #task
    path("Task_create/",views.Task_create,name="Task_create"),
    path("Task_list/",views.Task_list,name="Task_list"),
    path("get_Task_details/",views.get_Task_details,name="get_Task_details"),
    path("Task_update/<str:task_name>/",views.Task_update,name="Task_update"),
    path("task_delete/<str:task_name>/",views.task_delete,name="task_delete"),
    #IndividualTask
    path("individualTask_create/",views.IndividualTask_create,name="IndividualTask_create"),
    path("IndividualTask_list/",views.IndividualTask_list,name="IndividualTask_list"),
    path("get_IndividualTask_details/",views.get_IndividualTask_details,name="get_IndividualTask_details"),
    path("IndividualTask_update/<str:Task_name>/",views.IndividualTask_update,name="IndividualTask_update"),
    path("IndividualTask_delete/<str:Task_name>/",views.IndividualTask_delete,name="IndividualTask_delete")
    
    

]