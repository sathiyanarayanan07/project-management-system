from django.db import models

# Create your models here.

class user(models.Model):
    user_image = models.ImageField(max_length=100,null=True,blank=True)
    username= models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank =True)
    Phone_number = models.CharField(max_length=10,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    role_type =models.CharField(max_length=100,default="employee")
    created_at = models.DateTimeField(auto_now_add=True)

class adminuser(models.Model):
    username= models.CharField(max_length=100,null=True,blank=True)
    password =models.CharField(max_length=100,null=True,blank=True)

class Team(models.Model):
    name =models.CharField(max_length=100,unique=True)
    description =models.TextField(max_length=100,null=True,blank=True)
    members= models.ManyToManyField(user,null=True,blank=True)