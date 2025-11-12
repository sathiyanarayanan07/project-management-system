from django.urls import path
from .import views   

urlpatterns = [
     path("user_list/",views.user_list,name="user_list"),
     path("Manager_list/",views.Manager_list,name="Manager_list"),
     #admin
     path("admin_update/<str:email>/",views.admin_update,name="admin_update"),
     path("Admin_list/",views.Admin_list,name="Admin_list"),
     path("Category_list/",views.Category_list,name="Category_list"),
     #category
     path("category_create/",views.category_create,name="category_create"),
     path("get_category/",views.get_category,name="get_category"),
     path("Category_update/<str:name>/",views.category_update,name="Category_update"),
     path("Category_delete/<str:name>/",views.Category_delete,name="Category_delete"),
     #phase_template
     path("create_phase_template/",views.create_phase_template,name="create_phase_template"),
     path("phase_template_list/",views.phase_template_list,name="phase_template_list"),
     path("phase_template_details/",views.phase_template_details,name="phase_template_details"),
     path("update_phase_template/<str:name>/",views.update_phase_template,name="update_phase_template"),
     path("Phase_template_delete/<str:name>/",views.Phase_template_delete,name="Phase_template_delete"),
    #login#
    path("single_login/",views.Single_login,name="single_login"),
    path("am_login/",views.AM_login,name="admin_manager_login"),
    #user#
    path("create_user/",views.register_user,name="create_user"),
    path("user_details/",views.user_details,name="user_details"),
    path("user_update/<str:email>/",views.user_update,name="user_update"),
    path("user_delete/<str:email>/",views.user_delete,name="user_delete"),

    #manager
    path("manager_details/",views.manager_details,name="manager_details"),
    path("manager_update/<str:email>",views.manager_update,name="manager_update"),
    path("Manager_delete/<str:email>/",views.Manager_delete,name="Manager_delete"),
  

    #team
    path("create_Team/",views.create_Team,name="create_Team"),
    path("team_list/",views.team_list,name="team_list"),
    path("get_team_details/",views.get_team_details,name="get_team_details"),
    path("team_delete/<str:name>/",views.team_delete,name="team_delete"),
    path("team_update/",views.team_update,name="team_update"),
    #project
    path("project_create/",views.project_create,name="project_create"),
    path("project_details/",views.project_details,name="project_details"),
    path("project_update/<str:name>/",views.project_update,name="project_update"),
    path("project_delete/<str:name>/",views.project_delete,name="project_delete"),
    #phase
    path("create_phases/",views.create_phases,name="create_phases"),
    path("get_phases_details/",views.get_phases_details,name="get_phases_details"),
    path("Phase_update/<str:role>/",views.Phase_update,name="Phase_update"),
    path("Phase_delete/<str:role>/",views.Phase_delete,name="Phase_delete"),

    path("create_teamleader_assignment/",views.create_teamleader_assignment,name="phaseassign_to_member"),
    path("get_teamleader_assignments/",views.get_teamleader_assignments,name="details_assign_to_members"),
    path("update_teamleader_assignment/<int:id>/",views.update_teamleader_assignment,name="update_to_assign"),
    path("delete_TeamLeaderAssignment/<int:id>/",views.delete_TeamLeaderAssignment,name="delete_members_assignment"),


    path("create_task/",views.create_task,name="create_task"),
    path("Task_details/",views.Task_details,name="Task_details"),
    path('update_task/<int:task_id>/', views.update_task,name="update_task"),
    path('delete_task/<int:task_id>/', views.delete_task,name="delete_task"),

    path("subtask_create/",views.subtask_create,name="subtask_create"),
    path("details_subtask/",views.details_subtask,name="details_subtask"),
    path("update_subtask/<str:name>/",views.update_subtask,name="update_subtask"),
    path("subtask_delete/<str:name>/",views.subtask_delete,name="subtask_delete"),
    path("get_categories_with_phases/", views.category_with_phases, name="get_categories_with_phases"),


    

]