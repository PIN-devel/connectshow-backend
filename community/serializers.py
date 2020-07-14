from rest_framework import serializers
from accounts.serializers import UserIdentifySerializer, ClubSerializer
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserIdentifySerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'image', 'created_at', 'updated_at', 'user')


class ArticleSerializer(serializers.ModelSerializer):
    user = UserIdentifySerializer(required=False)
    club = ClubSerializer(required=False)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user', 'club')


class CommentListSerializer(serializers.ModelSerializer):
    user = UserIdentifySerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'updated_at', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = UserIdentifySerializer(required=False)
    article = ArticleSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at',
                            'updated_at', 'user', 'article')
