from rest_framework import serializers
from .models import user,Manager,TeamLeader,Admin,Team,Phase,project,TeamLeaderAssignment,Category,Task

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields ="__all__"


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields ="__all__"


class TeamLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields ="__all__"


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields ="__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields ="__all__"



class projectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields ="__all__"




class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields ="__all__"


class teamleader_to_membersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeaderAssignment
        fields ="__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ="__all__"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields ="__all__"