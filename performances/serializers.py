from rest_framework import serializers

from .models import Performance, Category, Review,Cast
from accounts.serializers import UserSerializer,UserIdentifySerializer,ClubSerializer
from accounts.models import Club

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('id', 'title', 'poster_image')


class PerformanceSerializer(serializers.ModelSerializer):
    # clubs = ClubSerializer(read_only=True, many=True)
    casts = UserIdentifySerializer(many=True)
    clubs = ClubSerializer(required=False, many=True)
    category = CategorySerializer(required=False)
    class Meta:
        model = Performance
        fields = '__all__'
        read_only_fields = ('id', 'clubs', 'created_at', 'updated_at', 'like_users', 'casts', 'avg_rank', 'category')

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    performance = PerformanceSerializer()
    class Meta:
        model = Review
        fields = ('id', 'point', 'content', 'user', 'performance')
    
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    performance = PerformanceSerializer(required=False)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

