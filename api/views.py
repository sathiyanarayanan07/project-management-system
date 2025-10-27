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
                     "password":password,
                     "role_type":role_type},status=200)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user  # replace with your actual model name (User, CustomUser, etc.)

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
             
  


       





