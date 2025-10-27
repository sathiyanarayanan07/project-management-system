from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user,adminuser,Team
from .serializers import userSerializer,adminuserSerializer,TeamSerializer
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
def user_profile(request,email):
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

     
     



     

             
  


       





