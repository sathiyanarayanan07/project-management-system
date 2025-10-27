from django.contrib import admin
from .models import user,adminuser,Team

# Register your models here.
admin.site.register(user)
admin.site.register(adminuser)
admin.site.register(Team)
