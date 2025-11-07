from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user,Manager,TeamLeader,Admin,Team,project,Phase,teamleader_to_members
from .serializers import userSerializer,ManagerSerializer,TeamLeaderSerializer,AdminSerializer,TeamSerializer,projectSerializer,PhaseSerializer,teamleader_to_membersSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import uuid


@api_view(['GET'])
def user_list(request):
     users=user.objects.all()
     serializer = userSerializer(user,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def team_list(request):
     users=Team.objects.all()
     serializer = TeamSerializer(users,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def Manager_list(request):
     users=Manager.objects.all()
     serializer = ManagerSerializer(Manager,many=True)
     return Response(serializer.data)



@api_view(['GET'])
def TeamLeader_list(request):
     users=TeamLeader.objects.all()
     serializer = TeamLeaderSerializer(TeamLeader,many=True)
     return Response(serializer.data)


@api_view(['GET'])
def Admin_list(request):
     users=Admin.objects.all()
     serializer = AdminSerializer(Admin,many=True)
     return Response(serializer.data)




@api_view(['POST'])
def Single_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    role_type = request.data.get("role_type")

    if not email or not password or not role_type:
        return Response({"msg": "invalid credentials"}, status=400)

    try:
        if role_type == "employee":
            login_user = user.objects.get(email=email, password=password, role_type=role_type)
        elif role_type == "Manager":
            login_user = Manager.objects.get(email=email, password=password, role_type=role_type)
        elif role_type == "TeamLeader":
            login_user = TeamLeader.objects.get(email=email, password=password, role_type=role_type)
        elif role_type == "Admin":
            login_user = Admin.objects.get(email=email, password=password, role_type=role_type)
        else:
            return Response({"msg": "invalid data"}, status=400)

     
        return Response({
            "msg": "login Successfully",
            "email": login_user.email,
            "role_type": login_user.role_type
        }, status=200)

    except ObjectDoesNotExist:
        return Response({"msg": "Invalid email or password"}, status=401)
    
@api_view(['POST'])
def register_user(request):
    username= request.data.get("username")
    email= request.data.get("email")
    Phone_number=request.data.get("Phone_number")
    role= request.data.get("role")
    password= request.data.get("password")
    role_type=request.data.get("role_type")

    if user.objects.filter(email=email).exists():
        return Response({"msg":"email already exists"},status=400)
    
    try:
        if role_type == "employee":
            create_user = user.objects.create(
                username=username,
                email=email,
                Phone_number=Phone_number,
                role=role,
                password=password,
                role_type=role_type

            )
        elif role_type == "Manager":
            create_manager = Manager.objects.create(
                 username=username,
                 email=email,
                 Phone_number=Phone_number,
                 password=password,
                 role_type=role_type
                 
            )
        elif role_type == "TeamLeader":
             create_TeamLeader =TeamLeader.objects.create(
                  username=username,
                  email=email,
                  Phone_number=Phone_number,
                  role=role,
                  password=password,
                  role_type=role_type
             )
        else:
            return Response({"msg":"invaild data"},status=400)
        token =str(uuid.uuid4())
        subject = "Your PMS Account Credentials",
        link ="/{token}/{email}"
        message = f"Hello {username},\n\nYour account has been created.\n\nemail: {email}\nPassword: {password}\n\nrole:{role_type}."
        send_mail(subject, message,link, None, [email])
        return Response({"msg":"manager create successfully",
                         "username":username,
                         "email":email,
                         "Phone_number":Phone_number,
                         "role":role,
                         "password":password,
                         "role_type":role_type
                         },status=200)
    except Exception as e:
        return Response({"msg": "Error creating user", "error": str(e)},
            status=500)



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
            "role":u.role,
            "created_at":u.created_at
        })

    return Response(data, status=200)



@api_view(['PUT'])
def user_update(request,email):
        try:
             user_instance = user.objects.get(email=email)
        except user.DoesNotExist:
             return Response({"msg":"user not found"},status=404)

        profile_image =request.FILES.get("profile_image")
        username= request.data.get("username")
        email= request.data.get("email")
        Phone_number = request.data.get("Phone_number")
        role =request.data.get("role")
        password = request.data.get("password")
        role_type = request.data.get("role_type")
        if profile_image:
              user_instance.profile_image = profile_image
        if username:
              user_instance.username= username
        if email:
          user_instance.email = email
        if Phone_number:
            user_instance.Phone_number = Phone_number
        if role:
             user_instance.role =role
        if password:
             user_instance.password = password
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
def manager_details(request):
    users = Manager.objects.all()

    if not Manager.exists():
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


@api_view(['PUT'])
def manager_update(request,email):
        try:
             user_instance = Manager.objects.get(email=email)
        except Manager.DoesNotExist:
             return Response({"msg":"user not found"},status=404)

        profile_image =request.FILES.get("profile_image")
        username= request.data.get("username")
        email= request.data.get("email")
        Phone_number = request.data.get("Phone_number")
        password = request.data.get("password")
        role_type = request.data.get("role_type")
        if profile_image:
              user_instance.user_image = profile_image
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
def Manager_delete(request,email):
     user_delete = Manager.objects.filter(email=email)
     if not user_delete:
          return Response({"msg":f"user {email}not found "},status=404)
     
     user_delete.delete()
     return Response({"msg":f"user {email} delete sucessfully"})

@api_view(['GET'])
def TeamLeader_details(request):
    users = TeamLeader.objects.all()

    if not TeamLeader:
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


@api_view(['PUT'])
def TeamLeader_update(request,email):
        try:
             user_instance = TeamLeader.objects.get(email=email)
        except TeamLeader.DoesNotExist:
             return Response({"msg":"user not found"},status=404)

        profile_image =request.FILES.get("profile_image")
        username= request.data.get("username")
        email= request.data.get("email")
        Phone_number = request.data.get("Phone_number")
        password = request.data.get("password")
        role_type = request.data.get("role_type")
        if profile_image:
              user_instance.user_image = profile_image
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
        serializer = TeamLeaderSerializer(user_instance)
        return Response(serializer.data, status=200)

@api_view(['DELETE'])
def TeamLeader_delete(request,email):
     user_delete = TeamLeader.objects.filter(email=email)
     if not user_delete:
          return Response({"msg":f"user {email}not found "},status=404)
     
     user_delete.delete()
     return Response({"msg":f"user {email} delete sucessfully"},status=200)

##admin login ##
@api_view(['POST'])
def admin_login(request):
     admin_name = request.data.get("admin_name")
     password= request.data.get("password")

     if not Admin or not password:
          return Response({"msg":"admin user not found"},status=404)
     
     admin_log = Admin.objects.get(
          admin_name=admin_name,
          password=password

   
     )
     return Response({"msg":"admin login sucessfully",
                      "admin_user":admin_name,
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
def get_team_details(request):
     team_view =Team.objects.all()
     if not team_view:
          return Response({"msg":"Team not found"},status=404)
     
     team_list=[]
     for get in team_view:
          team_list.append({
               "name":get.name,
               "description":get.description,
               "members":list(get.members.values_list("username"))
          })
     return Response(team_list)


#team Delete
@api_view(['DELETE'])
def team_delete(request,name):
     try:
          team_del = Team.objects.get(name=name).first()
          team_del.delete()
          if not team_del:
               return Response({"msg":"team not found"},status=404)
     except Team.DoesNotExist:
          return Response({"msg":"Team Delete Successfully"},status=200)

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

#project
@api_view(['POST'])
def project_create(request):
     try:
          data = request.data
          name = data.get("name")
          description=data.get("description")
          priority=data.get("priority")
          start_date=data.get("start_date")
          End_date =data.get("End_date")
          status=data.get("status")

          create_project =project.objects.create(
               name=name,
               description=description,
               priority=priority,
               start_date=start_date,
               End_date=End_date,
               status=status

          )
          return Response({"msg":"project create successfully",
                           "name":name,
                           "description":description,
                           "priority":priority,
                           "start_date":start_date,
                           "End_date":End_date,
                            "status":status },status=200)
     except project.DoesNotExist:
          return Response({"msg":"invaild data"},status=400)
     

@api_view(['GET'])
def project_details(request):
     project_get =project.objects.all()
     if not project_get:
          return Response({"msg":"project detail not found"},status=404)
     
     proj_list=[]
     for pro in project_get:
          proj_list.append({
               "name":pro.name,
               "description":pro.description,
               "priority":pro.priority,
               "start_date":pro.start_date,
               "End_date":pro.End_date,
               "status":pro.status,
               "create_at":pro.create_at
               
          })
     return Response(proj_list,status=200)


@api_view(['PUT'])
def project_update(request,name):
      try:
             project_instance = project.objects.get(name=name)
      except project.DoesNotExist:
             return Response({"msg":"project instance not found"},status=404)
      
      name =request.data.get("name")
      description= request.data.get("description")
      priority= request.data.get("priority")
      start_date = request.data.get("start_date")
      End_date =request.data.get("End_date")
      status = request.data.get("status")
      if name:
           project_instance.name = name
      if description:
              project_instance.description= description
      if priority:
          project_instance.priority = priority
      if start_date:
            project_instance.start_date = start_date
      if End_date:
             project_instance.End_date =End_date
      if status:
             project_instance.status = status
             project_instance.save()
             serializer = userSerializer(project_instance)
             return Response(serializer.data, status=200)



@api_view(['DELETE'])
def project_delete(request,name):
     project_delete = project.objects.filter(name=name)
     if not project_delete:
          return Response({"msg":f"user {name}not found "},status=404)
     
     project_delete.delete()
     return Response({"msg":f"user {name} delete sucessfully"})




#project_phases#
@api_view(['POST'])
def create_phases(request):
     project_name =request.data.get("project")
     role= request.data.get("role")
     team_leader_id =request.data.get("team_leader")
     status = request.data.get("status")
     start_date = request.data.get("start_date")
     end_date = request.data.get("end_date")

     project_instance = project.objects.get(name=project_name)
     if not project_instance:
          return Response({"msg":"project not found"},status=404)
     TL_instance =user.objects.get(id=team_leader_id)
     if not TL_instance:
          return Response({"msg":"user not found"},status=404)
  
     
     if TL_instance.role_type!="TeamLeader":
          TL_instance.role_type = "TeamLeader"
          TL_instance.save()

     if not TeamLeader.objects.filter(email=TL_instance.email).exists():
            TeamLeader.objects.create(
                profile_image=TL_instance.profile_image,
                username=TL_instance.username,
                email=TL_instance.email,
                Phone_number=TL_instance.Phone_number,
                password=TL_instance.password,
                role_type="TeamLeader"
            )
     
     create_phases= Phase.objects.create(
        project=project_instance,
        role=role,
        team_leader=TL_instance,
        status=status,
        start_date= start_date,
        end_date=end_date

     )
     return Response({"msg":"phases create sucessfully"},status=200)




@api_view(['GET'])
def get_phases_details(request):
     phase_obj =Phase.objects.all()
     if not phase_obj:
          return Response({"msg":"phase is not found"},status=400)
     
     phase_list=[]
     for phas in phase_obj:
          phase_list.append({
               "project":phas.project.name,
               "description":phas.project.description,
               "role":phas.role,
               "team_leader":phas.team_leader.username if phas.team_leader else None,
               "priority":phas.project.priority,
               "status":phas.status,
               "progress":phas.progress,
               "start_date":phas.start_date,
               "end_date":phas.end_date



          })
     return Response(phase_list,status=200)



@api_view(['PUT'])
def Phase_update(request, role):
    try:
        Phase_instance = Phase.objects.get(role=role)
    except Phase.DoesNotExist:
        return Response({"msg": "Phase instance not found"}, status=404)

    project_name = request.data.get("project")
    new_role = request.data.get("role")
    team_leader_name = request.data.get("team_leader")
    status = request.data.get("status")
    progress = request.data.get("progress")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    if project_name:
        try:
            project_instance = project.objects.get(name=project_name)
            Phase_instance.project = project_instance
        except project.DoesNotExist:
            return Response({"msg": "Project not found"}, status=404)

    if team_leader_name:
        try:
            team_leader_instance = user.objects.get(username=team_leader_name)
            Phase_instance.team_leader = team_leader_instance
        except user.DoesNotExist:
            return Response({"msg": "Team Leader not found"}, status=404)

    # Update other fields
    if new_role:
        Phase_instance.role = new_role
    if status:
        Phase_instance.status = status
    if progress:
        Phase_instance.progress = progress
    if start_date:
        Phase_instance.start_date = start_date
    if end_date:
        Phase_instance.end_date = end_date

    Phase_instance.save()
    serializer = PhaseSerializer(Phase_instance)
    return Response(serializer.data, status=200)


#phases#
@api_view(['POST'])
def teamleader_assign_to_member(request):
          phase_id =request.data.get("Phase")
          assigned_to_username = request.data.get("assigned_to")
          status= request.data.get("status")
          try:
               phase_instance =Phase.objects.get(id=phase_id)
          except Phase.DoesNotexist:
               return Response({"msg":"phase not found"},status=404)
          try:
               member_instance =user.objects.get(username=assigned_to_username)
          except user.DoesNotExist:
               return Response({"msg":"user not found"},status=404)
          
          assign_phase = teamleader_to_members.objects.create(
               Phase=phase_instance,
               assigned_to=member_instance,
               status=status
          )
          return Response({"msg":"phase assign to team member",
                           "Phase":phase_instance.id,
                           "assigned_to_member":member_instance.username,
                           "status":status},status=200)
          

@api_view(['GET'])
def teamleader_to_member(request):
     assignments =teamleader_to_members.objects.all()
     if not assignments:
          return Response({"msg":"assign member not found"},status=404)
     
     get=[]
     for a in assignments:
          get.append({
               "Phase":a.Phase.project.name,
               "assigned_to":a.assigned_to.username,
               "status":a.status,
               "start_date":a.Phase.start_date,
               "end_date":a.Phase.end_date

          })
     return Response(get,status=200)
     








    