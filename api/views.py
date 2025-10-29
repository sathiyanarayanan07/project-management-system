from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user,adminuser,Team,Project,Task
from .serializers import userSerializer,adminuserSerializer,TeamSerializer,ProjectSerializer,TaskSerializer
from django.core.mail import send_mail

# Create your views here.

@api_view(['POST'])
def user_register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    Phone_number= request.data.get("Phone_number")
    password = request.data.get("password")
    role_type = request.data.get("role_type")
     
    if not username or not email or not password or not role_type:
        return Response({"msg":" please fill the details"},status=404)
    
    if len(password) < 8:
         return Response({"message":"password must be at least 8 characters"},status=400)
            
    
    if role_type == "employee":
        create_user=user.objects.create(
        username=username,
        email=email,
        Phone_number=Phone_number,
        password=password,
        role_type=role_type
    )
    else:
        return Response({"msg":"invaild data"},status=404)
    
    subject = "Your PMS Account Credentials"
    message = f"Hello {username},\n\nYour account has been created.\n\nemail: {email}\nPassword: {password}\n\n."
    send_mail(subject, message, None, [email])
    
    return Response({"msg":"user register sucessfully",
                     "username":username,
                     "email":email,
                     "Phone_number":Phone_number,
                     "password":password,
                     "role_type":role_type},status=200)

@api_view(['GET'])
def user_list(request):
     users=user.objects.all()
     serializer = userSerializer(users,many=True)
     return Response(serializer.data)

@api_view(['GET'])
def user_details(request):
    users = user.objects.all()

    if not users.exists():
        return Response({"msg": "No users found"}, status=404)

    data = []
    for u in users:
        data.append({
            "username": u.username,
            "email": u.email,
            "password":u.password,
            "created_at":u.created_at
        })

    return Response(data, status=200)



@api_view(['POST'])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    role_type = request.data.get("role_type")
    
    if role_type == "employee":
            login= user.objects.get(
            email=email,
            password=password,
            role_type= role_type)
    else:
         return Response({"msg":"invalid credentials"},status=404)
    
    return Response({"msg":"login successfully",
                     "email":email,
                     "role_type":role_type},status=200)

@api_view(['PUT'])
def user_update(request,email):
        try:
             user_instance = user.objects.get(email=email)
        except user.DoesNotExist:
             return Response({"msg":"user not found"},status=404)

        user_image =request.FILES.get("user_image")
        username= request.data.get("username")
        email= request.data.get("email")
        Phone_number = request.data.get("Phone_number")
        password = request.data.get("password")
        role_type = request.data.get("role_type")
        if user_image:
              user_instance.user_image = user_image
        if username:
              user_instance.username= username
        if email:
          user_instance.email = email
        if Phone_number:
            user_instance.Phone_number = Phone_number
        if password:
             user_instance.password = password
        if role_type:
             user_instance.role_type = role_type
        user_instance.save()
        serializer = userSerializer(user_instance)
        return Response(serializer.data, status=200)

@api_view(['DELETE'])
def user_delete(request,email):
     user_delete = user.objects.filter(email=email)
     if not user_delete:
          return Response({"msg":f"user {email}not found "},status=404)
     
     user_delete.delete()
     return Response({"msg":f"user {email} delete sucessfully"})

@api_view(['GET'])
def user_profile_details(request):
     profile_details = user.objects.all()

     if not profile_details:
          return Response({"msg":"user profile details not found"},status=404)
     
     user_pro =[]
     for up in profile_details:
          user_pro.append({
               "username":up.username,
               "email":up.email,
               "Phone_number":up.Phone_number,
               "password":up.password,
               "role_type":up.role_type

          })
          return Response(user_pro, status=200)
     

##admin login ##
@api_view(['POST'])
def admin_login(request):
     admin_user = request.data.get("admin_user")
     password= request.data.get("password")

     if not adminuser or not password:
          return Response({"msg":"admin user not found"},status=404)
     
     admin_log = adminuser.objects.get(
          admin_user=admin_user,
          password=password

   
     )
     return Response({"msg":"admin login sucessfully",
                      "admin_user":admin_user,
                      "password":password},status=200)

##Team_create#
@api_view(['POST'])
def create_Team(request):
     name=request.data.get("name")
     description=request.data.get("description")
     members_name = request.data.get("members",[])

     if not name or not description or not members_name:
          return Response({"msg":"please fill the all requied fields"},status=404)
     
     

     team_create = Team.objects.create(
          name = name,
          description= description
     )
     members =[]
     for name in members_name:
          try:
            user_name=user.objects.get(username=name)
            members.append(user_name)
          except user.DoesNotExist:
               return Response({"msg":F"user with name{name} not found"},status=404)

     team_create.members.add(*members)
     team_create.save()

     return Response({"msg":"Team create sucessfully",
                      "name":name,
                      "description":description,
                      "members": members_name},status=200)

@api_view(['GET'])
def team_list(request):
     users=Team.objects.all()
     serializer = TeamSerializer(users,many=True)
     return Response(serializer.data)

@api_view(['GET'])
def get_team_details(request):
     team_view =Team.objects.all()
     if not team_view:
          return Response({"msg":"Team not found"},status=404)
     
     team_list=[]
     for get in team_view:
          team_list.append({
               "name":get.name,
               "description":get.description,
               "members":list(get.members.values_list("username",flat=True))
          })
     return Response(team_list)

##Team remove ##
@api_view(['POST'])
def remove_team_member(request):
     team_name = request.data.get("team_name")
     member_name = request.data.get("member_name")

     if not team_name or not member_name:
          return Response({"msg":"please provide both team_name and member_name"},status=400)
     
     try:
          team = Team.objects.get(name=team_name)
     except Team.DoesNotExist:
          return Response({"msg":f"Team'{team_name}'not found"},status=404)
     
     try:
          member = user.objects.get(username=member_name)
     except user.DoesNotExist:
          return Response({"msg":F"user '{member_name}not found"},status=404)
     
     team.members.remove(member)
     team.save()

     return Response({"msg":f"User {team_name} removed from team {member_name} successfully"},status=200)


##team update##
@api_view(['PUT'])
def team_update(request):
     team_name = request.data.get("team_name")
     new_description =request.data.get("description")
     member_emails = request.data.get("members",[])

     if not team_name:
          return Response({"msg":"please provide the existing team_name"},status=404)
     
     try:
          team = Team.objects.get(name=team_name)
     except Team.DoesNotExist:
          return Response({"msg":f"Team'{team_name}'not found"},status=404)
     
  
     if new_description:
          team.description = new_description


     if member_emails:
        members = []
        for email in member_emails:
            matching_users = user.objects.filter(email=email)
            if not matching_users.exists():
                return Response({"msg": f"User with email '{email}' not found"}, status=404)
            members.extend(matching_users)
        team.members.set(members)

     return Response({
        "msg": "Team updated successfully",
        "team_name": team.name,
        "description": team.description,
        "members": [m.email for m in team.members.all()]
    }, status=200)


#create project#
@api_view(['POST'])
def create_project(request):
     project_name =request.data.get("project_name")
     description = request.data.get("description")
     team_name= request.data.get("team")
     members_name= request.data.get("members", [])
     status =request.data.get("status")
     start_date =request.data.get("start_date")
     end_date = request.data.get("end_date")

     if not project_name:
          return Response({"msg":"project name is required"},status=404)
     if not team_name:
          return Response({"msg":"Team name is required"},status=404)
     if Project.objects.filter(project_name=project_name).exists():
          return Response({"msg":"project is already exists"},status=404)

     
     team_obj =Team.objects.get(name=team_name)
     if not team_obj:
          return Response({"team is not found"},status=404)
     
     project_create = Project.objects.create(
          project_name=project_name,
          description=description,
          team =team_obj,
          status=status,
          start_date=start_date,
          end_date=end_date

     )

     member=[]
     for mem in members_name:
          try:
               user_obj =user.objects.get(username=mem)
               member.append(user_obj)
          except user.DoesNotExist:
               return Response({"msg":f"user with name{members_name} not found"},status=404)
     project_create.members.add(*member)
     project_create.save()
     
     return Response({"msg":"project create sucessfully",
                      "project_name":project_name,
                      "description":description,
                      "team_name":team_name,
                      "members":members_name,
                      "status":status,
                      "start_date":start_date,
                      "end_date":end_date
                      },status=200)

@api_view(['GET'])
def project_list(request):
     pro_list=Project.objects.all()
     serializer = ProjectSerializer(pro_list,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def get_project_details(request):
     Project_view =Project.objects.all()
     if not Project_view:
          return Response({"msg":"Project view not found"},status=404)
     
     project_list=[]
     for get in Project_view:
          project_list.append({
               "project_name":get.project_name,
               "description":get.description,
               "team":get.team.name,
               "status":get.status,
               "members":list(get.members.values_list("username",flat=True)),
               "start_date":get.start_date,
               "end_date":get.end_date,
               "created_at":get.created_at
          })
     return Response(project_list)


#delete project
@api_view(['DELETE'])
def project_delete(request,name):
     projects= Project.objects.filter(project_name=name)
     if not project_delete:
          return Response({"msg":f"project {projects} not found"},status=404)
     projects.delete()

     return Response({"msg":f"project name is {name} delete successfully"},status=200)

#projectupdate#
@api_view(['PATCH'])
def project_update(request,project_name):
     try:
          project_instance =Project.objects.get(project_name=project_name)
     except Project.DoesNotExist:
          return Response({"msg":"project is not found"},status=404)

     project_name= request.data.get("project_name")
     description = request.data.get("description")
     team_name= request.data.get("team")
     status= request.data.get("status")
     members_list= request.data.get("members")
     start_date = request.data.get("start_date")
     end_date = request.data.get("end_date")

       


     if project_name:
          project_instance.project_name= project_name
     if description:
          project_instance.description= description
     if status:
          project_instance.status = status
     if start_date:
          project_instance.start_date = start_date
     if end_date:
          project_instance.end_date = end_date

     if team_name:
          try:
               team_obj = Team.objects.get(name=team_name)
          except Team.DoesNotExist:
               return Response({"msg":"team is not found"},status=404)
          project_instance.team = team_obj
     
     if members_list:
          member =[]
          for username in members_list:
               try:
                    user_obj =user.objects.get(username=username)
                    member.append(user_obj)
               except user.DoesNotExist:
                    return Response({"msg":"user not found"},status=404)
          project_instance.members.set(member)
     project_instance.save()
     serializer =ProjectSerializer(project_instance)
     return Response(serializer.data, status=200)


#Task#
@api_view(['POST'])
def Task_create(request):
     task_name= request.data.get("task_name")
     task_inform= request.data.get("task_inform")
     member_name= request.data.get("task_member")
     start_date = request.data.get("start_date")
     deadline = request.data.get("deadline")
     status = request.data.get("status")
          
     assign_task= user.objects.get(username=member_name)
     if not assign_task:
          return Response({"msg":"user member not found"},status=404)
          
     task_create= Task.objects.create(
          task_name=task_name,
          task_inform=task_inform,
          task_member=assign_task,
          start_date=start_date,
          deadline=deadline,
          status=status

          )
     return Response({"msg":"Task create sucessfully",
                       "Task_name":task_name,
                       "Task_inform":task_inform,
                       "Task_member":member_name,
                       "Start_date":start_date,
                       "deadline":deadline,
                       "status":status
                       },status=200)


@api_view(['GET'])
def Task_list(request):
     users=Task.objects.all()
     serializer = TaskSerializer(users,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def get_Task_details(request):
     Task_view =Task.objects.all()
     if not Task_view:
          return Response({"msg":"Task view not found"},status=404)
     
     Task_list=[]
     for get in Task_view:
          Task_list.append({
               "task_name":get.task_name,
               "Task_inform":get.task_inform,
               "Task_member":get.task_member.username,
               "start_date":get.start_date,
               "deadline":get.deadline,
               "status":get.status
          })
     return Response(Task_list)


@api_view(['PATCH'])
def Task_update(request,task_name):
     try:
          task_instance =Task.objects.get(task_name=task_name)
     except Task.DoesNotExist:
          return Response({"msg":"Task is not found"},status=404)

     task_name= request.data.get("task_name")
     task_inform = request.data.get("task_inform")
     member_name= request.data.get("task_member")
     start_date= request.data.get("start_date")
     deadline= request.data.get("deadline")
     status = request.data.get("status")
     notes = request.data.get("notes")




     if task_name:
          task_instance.task_name= task_name
     if task_inform:
          task_instance.task_inform= task_inform
    
     if start_date:
          task_instance.start_date = start_date
     if deadline:
          task_instance.deadline = deadline
     if status:
          task_instance.status= status
     if notes:
          task_instance.notes = notes


     if member_name:
          try:
               assign_user = user.objects.get(username=member_name)
          except user.DoesNotExist:
               return Response({"msg":"user is not found"},status=404)
          task_instance.task_member =assign_user
     task_instance.save()
     serializer = TaskSerializer(task_instance)
     return Response(serializer.data, status=200)

@api_view(['DELETE'])
def task_delete(request,task_name):
     task_del =Task.objects.get(task_name=task_name).delete()
     if not task_del:
          return Response({"msg":"task is not found"},status=404)
     return Response({"msg":"task delete successfully"},status=200)



















     

     
     

          
     


     
     



     

             
  


       




