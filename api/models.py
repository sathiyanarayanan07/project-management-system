from django.db import models

# Create your models here.


class user(models.Model):
    profile_image = models.ImageField(upload_to="profile_image/",null=True,blank=True)
    username= models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank =True)
    Phone_number = models.CharField(max_length=10,null=True,blank=True)
    role = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    role_type =models.CharField(max_length=100,default="employee")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}-{self.id}--{self.role}"
    

class Manager(models.Model):
    profile_image =models.ImageField(upload_to="profile_image/",null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    Phone_number = models.CharField(max_length=100,null=True,blank=True)
    password =models.CharField(max_length=100,null=True,blank=True)
    role_type =models.CharField(max_length=100,null=True,blank=True,default="Manager")
    created_at =models.DateTimeField(auto_now_add=True)

class TeamLeader(models.Model):
    profile_image =models.ImageField(upload_to="profile_image/",null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    Phone_number = models.CharField(max_length=100,null=True,blank=True)
    role = models.CharField(max_length=100,null=True,blank=True)
    password =models.CharField(max_length=100,null=True,blank=True)
    role_type =models.CharField(max_length=100,null=True,blank=True,default="TeamLeader")
    created_at =models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    admin_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    role_type = models.CharField(max_length=100,null=True,blank=True,default="Admin")
    password = models.CharField(max_length=100,null=True,blank=True)

    
class Team(models.Model):
    name =models.CharField(max_length=100,null=True,blank=True,unique=True)
    description =models.TextField(max_length=100,null=True,blank=True)
    members= models.ManyToManyField(user,blank=True)
  


    def __str__(self):
        return f"{self.name}--{self.description}"
    

class project(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description =models.TextField(null=True,blank=True)
    priority =models.CharField(max_length=100,null=True,blank=True,default="small")
    start_date =models.DateField(null=True,blank=True)
    End_date =models.DateField(null=True,blank=True)
    status =models.CharField(max_length=50,null=True,blank=True,default="To do")
    create_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Phase(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE, related_name='phases')
    role= models.CharField(max_length=50,null=True,blank=True,default="Design")
    team_leader = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")
    progress = models.IntegerField(null=True,blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.role} -{self.project}--{self.id}"


class teamleader_to_members(models.Model):
    Phase =models.ForeignKey(Phase,on_delete=models.CASCADE,null=True,blank=True,related_name="assignment")
    assigned_to =models.ForeignKey(user,on_delete=models.CASCADE,null=True,blank=True)
    status =models.CharField(max_length=100,null=True,blank=True)
    created_at =models.DateTimeField(auto_now=True)


