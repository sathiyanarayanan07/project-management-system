from django.contrib import admin
from .models import user,Manager,Admin,Team,project,Phase,TeamLeaderAssignment,Category,Task,subTask,phase_template,persontask

# Register your models here.
admin.site.register(user)
admin.site.register(Admin)
admin.site.register(Manager)
admin.site.register(Team)
admin.site.register(project)
admin.site.register(Phase)
admin.site.register(TeamLeaderAssignment)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(subTask)
admin.site.register(phase_template)
admin.site.register(persontask)



