from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Club
from performances.models import Performance, Category

User = get_user_model()

# ------------------------------------------------------------------


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('id', 'title', 'poster_image', 'end_date')
# ------------------------------------------------------------------


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'club_name', 'club_image')


class UserSerializer(serializers.ModelSerializer):
    like_categories = CategorySerializer(many=True)
    like_performances = PerformanceListSerializer(many=True)
    clubs = ClubSerializer(many=True)

    performances = PerformanceListSerializer(many=True)
    follow_clubs = ClubSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image',
                  'clubs', 'like_categories', 'like_performances', 'follow_clubs', 'performances')
        read_only_fields = ('id', 'username')


class UserIdentifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')
        read_only_fields = ('id', 'username')


class ClubSerializer(serializers.ModelSerializer):
    master = UserIdentifySerializer(required=False)
    members = UserIdentifySerializer(required=False, many=True)

    class Meta:
        model = Club
        fields = '__all__'
