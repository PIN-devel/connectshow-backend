from rest_framework import serializers
from accounts.serializers import UserSerializer, ClubSerializer
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    club = ClubSerializer()

    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    club = ClubSerializer(required=False)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user', 'club')


class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    article = ArticleSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    article = ArticleSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at',
                            'updated_at', 'user', 'article')
