from django.db import models

# Create your models here.


class user(models.Model):
    user_image = models.ImageField(upload_to="user_image/",null=True,blank=True)
    username= models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank =True)
    Phone_number = models.CharField(max_length=10,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    role_type =models.CharField(max_length=100,default="employee")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class Team(models.Model):
    name =models.CharField(max_length=100,null=True,blank=True,unique=True)
    description =models.TextField(max_length=100,null=True,blank=True)
    members= models.ManyToManyField(user,blank=True)

    def __str__(self):
        return f"{self.name}--{self.description}"

class adminuser(models.Model):
    admin_user= models.CharField(max_length=100,null=True,blank=True)
    password =models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.admin_user


    
class Project(models.Model):
    project_name = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    team= models.ForeignKey(Team,null=True,blank=True,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,null=True,blank=True,default="planning")
    members= models.ManyToManyField(user,blank=True)
    progress =models.PositiveIntegerField(default=0)
    start_date= models.DateField(null=True,blank=True)
    end_date =models.DateField(null=True,blank=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
    
class Task(models.Model):
    project =models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    task_name = models.CharField(max_length=100,null=True,blank=True)
    task_inform = models.TextField(null=True,blank=True)
    task_members =models.ManyToManyField(user,blank=True)
    start_date =models.DateField(null=True,blank=True)
    deadline = models.DateField(null=True,blank=True)
    progress = models.PositiveIntegerField(default=0)
    priority =models.CharField(default="medium")
    status = models.CharField(max_length=20,null=True,blank=True,default="open")
    notes = models.TextField(null=True,blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name
    
class IndividualTask(models.Model):
    Task_name =models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    members =models.ManyToManyField(user,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date =models.DateField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True,default="open")
    process =models.PositiveIntegerField(null=True,blank=True,default=0)
    notes =models.TextField(null=True,blank=True)

    def __str__(self):
        return self.Task_name
    

    

    



