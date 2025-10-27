from rest_framework import serializers
from .models import user,adminuser,Team

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields ="__all__"

class adminuserSerializer(serializers.ModelSerializer):
    class Meta:
        model =adminuser
        fields ="__all__"

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Team
        fields ="__all__"