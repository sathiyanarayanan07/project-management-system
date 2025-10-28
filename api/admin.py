from django.contrib import admin
from .models import user,adminuser,Team,Project

# Register your models here.
admin.site.register(user)
admin.site.register(adminuser)
admin.site.register(Team)
admin.site.register(Project)