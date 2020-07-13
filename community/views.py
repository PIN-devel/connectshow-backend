from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer, CommentListSerializer
from accounts.models import Club

PER_PAGE = 5

# Articles
@api_view(['GET', 'POST'])
def list_or_create(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    
    if request.method == 'GET':
        p = request.GET.get('_page', 1)
        articles = Paginator(Article.objects.filter(club=club).order_by('-id'), PER_PAGE)
        serializer = ArticleListSerializer(articles.page(p), many=True)
        articles_num = Article.objects.filter(club=club).count()
        return Response({"status": "OK", "data": serializer.data, 'articles_num': articles_num})

    else:
        if request.user.is_authenticated:
            if request.user == club.master:
                serializer = ArticleSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(user=request.user, club=club)
                    return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "클럽 마스터만 글을 작성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_or_update_or_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'GET':
        serializer = ArticleListSerializer(article)
        return Response({"status": "OK", "data": serializer.data})

    if request.user.is_authenticated:
        if request.method == 'DELETE':
            if request.user == article.user:
                article.delete()
                return Response({"status": "OK"})
            else:
                return Response({"status": "FAIL", "error_msg": "클럽 마스터만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        else:
            if request.user == article.user:
                serializer = ArticleSerializer(
                    article, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "클럽 마스터만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"status": "FAIL", "error_msg": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def comment_list_or_create(request, article_id):
    if request.method == 'GET':
        p = request.GET.get('_page', 1)
        comments = Paginator(Comment.objects.filter(
            article_id=article_id), PER_PAGE)
        serializer = CommentListSerializer(comments.page(p), many=True)
        comments_num = Comment.objects.filter(article_id=article_id).count()
        return Response({"status": "OK", "data": serializer.data, 'comments_num': comments_num})

    else:
        if request.user.is_authenticated:
            article = get_object_or_404(Article, id=article_id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, article=article)
                return Response({"status": "OK", "data": serializer.data})
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_update_or_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'DELETE':
        if request.user == comment.user:
            comment.delete()
            return Response({"status": "OK"})
        else:
            return Response({"status": "FAIL", "error_msg": "본인 댓글만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    else:
        if request.user == comment.user:
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"status": "OK", "data": serializer.data})
        else:
            return Response({"status": "FAIL", "error_msg": "본인 댓글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
