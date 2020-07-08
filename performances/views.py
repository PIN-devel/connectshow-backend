from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Performance, Review, Category
from accounts.models import Club
from .serializers import PerformanceListSerializer, PerformanceSerializer, ReviewListSerializer, ReviewSerializer

PER_PAGE = 10

@api_view(['GET', 'POST'])
def list_or_create(request):
    if request.method == 'GET':
        p = request.GET.get('page', 1)
        performances = Paginator(Performance.objects.order_by('-pk'),PER_PAGE)
        serializer = PerformanceListSerializer(performances.page(p), many=True)
        return Response({"status": "OK", "data": serializer.data})
    else:
        if request.user.is_authenticated:
            user_club = request.user.my_club.all()
            if user_club:
                serializer = PerformanceSerializer(data=request.data)
                category_id = request.data.get('category_id')
                club_id = request.data.get('club_id')
                category = get_object_or_404(Category, id=category_id)
                clubs = Club.objects.filter(id=club_id)
                if serializer.is_valid(raise_exception=True):
                    # club_id = request.data.get('club_id')
                    # serializer.object.clubs.add(user_club[0]) # 첫번째 클럽
                    # print(serializer.data.id)
                    serializer.save(clubs=clubs, category=category)
                    return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "Club의 관리자가 아닙니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'DELETE', 'PUT'])
def detail_or_delete_or_update(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)
    masters = []
    for master in list(performance.clubs.values('master')):
        masters.append(master['master'])
    if request.method == 'GET':
        serializer = PerformanceSerializer(performance)
        return Response({"status": "OK", "data": serializer.data})
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if request.user.id in masters:
                performance.delete()
                return Response({"status": "OK"})
            else:
                return Response({"status": "FAIL", "error_msg": "해당 관리자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if request.user.is_authenticated:
            if request.user.id in masters:
                # performance.title = request.data.get('title')
                # performance.start_date = request.data.get('start_date')
                # performance.end_date = request.data.get('end_date')
                # performance.running_time = request.data.get('running_time')
                # performance.time = request.data.get('time')
                # performance.poster_image = request.data.get('poster_image')
                # performance.description = request.data.get('description')
                # performance.url = request.data.get('url')
                # performance.category = request.data.get('category')
                # performance.save()
                serializer = PerformanceSerializer(
                    performance, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "해당 관리자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def recommend_performance(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_performance(request, performance_id):
    performance = get_object_or_404(Performance, pk=performance_id)
    if performance.like_users.filter(id=request.user.pk).exists():
        performance.like_users.remove(request.user)
        liked = False
    else:
        performance.like_users.add(request.user)
        liked = True
    context = {
        'liked': liked,
        'count': performance.like_users.count(),
    }
    return Response({"status": "OK", "data": context})


@api_view(['GET', 'POST'])
def review_list_or_create(request, performance_id):
    if request.method == 'GET':
        p = request.GET.get('page',1)
        reviews = Paginator(Review.objects.filter(performance_id=performance_id), PER_PAGE)
        serializer = ReviewListSerializer(reviews.page(p), many=True)
        return Response({"status": "OK", "data": serializer.data})
    else:
        if request.user.is_authenticated:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, performance=get_object_or_404(
                    Performance, id=performance_id))
                return Response({"status": "OK", "data": serializer.data})
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def review_update_or_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'DELETE':
        if request.user == review.user:
            review.delete()
            return Response({"status": "OK"})
        else:
            return Response({"status": "FAIL", "error_msg": "본인 Review만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    else:
        if request.user == review.user:
            review.point = request.data.get('point')
            review.content = request.data.get('content')
            review.save()
            serializer = ReviewSerializer(review)
            return Response({"status": "OK", "data": serializer.data})
        else:
            return Response({"status": "FAIL", "error_msg": "본인 Review만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
