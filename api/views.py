from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user,Manager,TeamLeader,Admin,Team,project,Phase,TeamLeaderAssignment,Category,Task
from .serializers import userSerializer,ManagerSerializer,TeamLeaderSerializer,AdminSerializer,TeamSerializer,projectSerializer,PhaseSerializer,teamleader_to_membersSerializer,CategorySerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import uuid


@api_view(['GET'])
def Category_list(request):
     users=Category.objects.all()
     serializer = CategorySerializer(users,many=True)
     return Response(serializer.data)

@api_view(['POST'])
def category_create(request):
     data=request.data
     name=request.data.get("name")
     description = data.get("description")

     if not name or not description:
          return Response({"msg":"please fill all required fields"},status=400)

     create_category=Category.objects.create(
          name=name,
          description=description
     )
     return Response({"msg":"create category successfully"},status=200)

@api_view(['DELETE'])
def Category_delete(request,name):
     Category_delete = Category.objects.filter(name=name)
     if not user_delete:
          return Response({"msg":f"category {name}not found "},status=404)
     
     Category_delete.delete()
     return Response({"msg":f"category {name} delete sucessfully"},status=200)




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
        elif role_type == "TeamLeader":
            login_user = TeamLeader.objects.get(email=email, password=password, role_type=role_type)
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
def AM_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    role_type = request.data.get("role_type")

    if not email or not password or not role_type:
        return Response({"msg": "invalid credentials"}, status=400)

    try:
        if role_type == "Manager":
            login_user = Manager.objects.get(email=email, password=password, role_type=role_type)
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
              user_instance.profile_image = profile_image
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
              user_instance.profile_image = profile_image
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
          category_name=data.get("category")
          status=data.get("status")

          try:
               category_instance =Category.objects.get(name=category_name)
          except Category.DoesNotExist:
               return Response({"msg":"category not found"},status=404)

          create_project =project.objects.create(
               name=name,
               description=description,
               priority=priority,
               start_date=start_date,
               category=category_instance,
               End_date=End_date,
               status=status

          )
          return Response({"msg":"project create successfully",
                           "name":name,
                           "description":description,
                           "priority":priority,
                           "start_date":start_date,
                           "category":category_name,
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
               "category":pro.category.name if pro.category else None,
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
     return Response({"msg":f"user {name} delete sucessfully"},status=200)




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
def Phase_update(request,role):
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


@api_view(['DELETE'])
def Phase_delete(request,role):
     Phase_delete = Phase.objects.filter(role=role)
     if not Phase_delete:
          return Response({"msg":f"user {role}not found "},status=404)
     
     Phase_delete.delete()
     return Response({"msg":f"user {role} delete sucessfully"})

@api_view(['POST'])
def create_teamleader_assignment(request):
    project_id = request.data.get("project")
    assigned_by_username = request.data.get("assigned_by")
    assigned_to_username = request.data.get("assigned_to")
    is_self_assigned = request.data.get("is_self_assigned", False)

    try:
        project_instance = project.objects.get(id=project_id)
    except project.DoesNotExist:
        return Response({"msg": "Project not found"}, status=404)

    try:
        assigned_by_instance = TeamLeader.objects.get(username=assigned_by_username)
    except TeamLeader.DoesNotExist:
        return Response({"msg": "Assigned_by user not found"}, status=404)

    try:
        assigned_to_instance = user.objects.get(username=assigned_to_username)
    except user.DoesNotExist:
        return Response({"msg": "Assigned_to user not found"}, status=404)


    assignment = TeamLeaderAssignment.objects.create(
        project=project_instance,
        assigned_by=assigned_by_instance,
        assigned_to=assigned_to_instance,
        is_self_assigned=is_self_assigned
    )

    serializer = teamleader_to_membersSerializer(assignment)
    return Response(serializer.data, status=201)

          

@api_view(['GET'])
def get_teamleader_assignments(request):
    assignments = TeamLeaderAssignment.objects.all()
    if not assignments:
        return Response({"msg": "No team leader assignments found"}, status=404)

    data = []
    for assignment in assignments:
        data.append({
            "project": assignment.project.name,
            "assigned_by": assignment.assigned_by.username,
            "assigned_to": assignment.assigned_to.username,
            "assigned_at": assignment.assigned_at,
            "is_self_assigned": assignment.is_self_assigned
        })

    return Response(data, status=200)


@api_view(['PUT'])
def update_teamleader_assignment(request, id):
    try:
        assignment = TeamLeaderAssignment.objects.get(id=id)
    except TeamLeaderAssignment.DoesNotExist:
        return Response({"msg": "Team leader assignment not found"}, status=404)

    project_id = request.data.get("project")
    assigned_by_username = request.data.get("assigned_by")
    assigned_to_username = request.data.get("assigned_to")
    is_self_assigned = request.data.get("is_self_assigned")

    if project_id:
        try:
            project_instance = project.objects.get(id=project_id)
            assignment.project = project_instance
        except project.DoesNotExist:
            return Response({"msg": "Project not found"}, status=404)

    if assigned_by_username:
        try:
            assigned_by_instance = TeamLeader.objects.get(username=assigned_by_username)
            assignment.assigned_by = assigned_by_instance
        except TeamLeader.DoesNotExist:
            return Response({"msg": "Assigned_by user not found"}, status=404)

    if assigned_to_username:
        try:
            assigned_to_instance = user.objects.get(username=assigned_to_username)
            assignment.assigned_to = assigned_to_instance
        except user.DoesNotExist:
            return Response({"msg": "Assigned_to user not found"}, status=404)

    if is_self_assigned is not None:
        assignment.is_self_assigned = bool(is_self_assigned)

    assignment.save()
    serializer = teamleader_to_membersSerializer(assignment)
    return Response(serializer.data, status=200)

@api_view(['DELETE'])
def delete_TeamLeaderAssignment(request,id):
     try:
         del_assign = TeamLeaderAssignment.objects.get(id=id)
         del_assign.delete()
         return Response({"msg":"delete successfully"},status=200)
     except TeamLeaderAssignment.DoesNotExist:
          return Response({"msg":"members not found"},status=404)
     


@api_view(['POST'])
def create_task(request):
    project_id = request.data.get("project")
    name = request.data.get("name")
    description = request.data.get("description")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")
    assigned_to_username = request.data.get("assigned_to")

    if not all([project_id, name, description, assigned_to_username]):
        return Response({"msg": "Please fill in all required fields"}, status=400)

    try:
        project_instance = project.objects.get(id=project_id)
    except project.DoesNotExist:
        return Response({"msg": "Project not found"}, status=404)

    try:
        assigned_to_instance = user.objects.get(username=assigned_to_username)
    except user.DoesNotExist:
        return Response({"msg": "Assigned user not found"}, status=404)

    task = Task.objects.create(
        project=project_instance,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        assigned_to=assigned_to_instance
    )

    return Response({
        "msg": "Task created successfully",
        "task_id": task.id
    }, status=201)