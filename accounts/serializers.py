from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Club 

User = get_user_model()

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id','club_name')
        #fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    clubs = ClubSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image','clubs')
        # fields = '__all__'
        read_only_fields = ('id', 'username', 'password')

class UserIdentifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        # fields = '__all__'
        read_only_fields = ('id', 'username', 'password')