from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Club 
from performances.serializers import CategorySerializer, PerformanceListSerializer

User = get_user_model()

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id','club_name')

class UserSerializer(serializers.ModelSerializer):
    like_categories = CategorySerializer(many=True)
    like_performances = PerformanceListSerializer(many=True)
    clubs = ClubSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image','clubs','like_categories','like_performances')
        read_only_fields = ('id', 'username')

class UserIdentifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = ('id', 'username')

# ------------------------------------------------------------------
class ClubSerializer(serializers.ModelSerializer):
    master = UserSerializer(required=False)
    members = UserIdentifySerializer(many=True)
    class Meta:
        model = Club
        fields = '__all__'
