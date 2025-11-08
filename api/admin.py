from django.contrib import admin
from .models import user,Manager,TeamLeader,Admin,Team,project,Phase,TeamLeaderAssignment

# Register your models here.
admin.site.register(user)
admin.site.register(Admin)
admin.site.register(TeamLeader)
admin.site.register(Manager)
admin.site.register(Team)
admin.site.register(project)
admin.site.register(Phase)
admin.site.register(TeamLeaderAssignment)

