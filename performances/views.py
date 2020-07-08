from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Performance, Review, Category, Cast
from accounts.models import Club, User
from .serializers import PerformanceListSerializer, PerformanceSerializer, ReviewListSerializer, ReviewSerializer

from django.db.models import Q
import datetime
from random import sample

PER_PAGE = 10
GHOST_ID = 1

@api_view(['GET', 'POST'])
def list_or_create(request):
    if request.method == 'GET':
        category_ids = request.GET.getlist('category_id')
        p = request.GET.get('page', 1)
        q = Q()
        for category_id in category_ids:
            q |= Q(category_id=int(category_id))
        latest_performances = Performance.objects.filter(q).filter(end_date__gte=datetime.datetime.today().date()).order_by('-start_date')
        performances = Paginator(latest_performances, PER_PAGE)
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
                # casts save
                user_ids = request.data.get('user_ids')
                non_user_names = request.data.get('non_user_names')
                if serializer.is_valid(raise_exception=True):
                    performance = serializer.save(clubs=clubs, category=category)
                   
                    user_casts =[]
                    non_user_casts=[]
                
                    if user_ids:
                        for user_id in user_ids:
                            username = User.objects.get(id=user_id).username
                            Cast.objects.create(performance=performance, user_id=user_id, is_user=True, name=User.objects.get(id=user_id).username)
                            user_casts.append({'user_id':user_id,'username':username})
                    if non_user_names:
                        for non_user_name in non_user_names:
                            username = non_user_name
                            Cast.objects.create(performance=performance, user_id=5, name=non_user_name)
                            non_user_casts.append({'username':username})
                    return Response({"status": "OK", "data": {'cast':{'user':user_casts,'non_user':non_user_casts},**serializer.data}})
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
        casts = Cast.objects.filter(performance=performance)
        user_casts =[]
        non_user_casts=[]
        for cast in casts:
            if cast.is_user:
                user_casts.append({'user_id':cast.user_id,'username':cast.name})
            else:
                non_user_casts.append({'username':cast.name})
        
        serializer = PerformanceSerializer(performance)
        return Response({"status": "OK", "data": {'cast':{'user':user_casts,'non_user':non_user_casts},**serializer.data}})
    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if request.user.id in masters:
                performance.delete()
                return Response({"status": "OK"})
            else:
                return Response({"status": "FAIL", "error_msg": "해당 관리자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
    else: # PUT
        if request.user.is_authenticated:
            if request.user.id in masters:
                serializer = PerformanceSerializer(performance, data=request.data, partial=True)
                
                user_ids = request.data.get('user_ids')
                non_user_names = request.data.get('non_user_names')
                if serializer.is_valid(raise_exception=True):
                    performance = serializer.save()                   
                    user_casts =[]
                    non_user_casts=[]
                    origin_casts = Cast.objects.filter(performance=performance)
                    if user_ids:
                        for user_id in user_ids:
                            # x -> o
                            print(Cast.objects.filter(performance_id=performance.id, user_id=user_id).exists())
                            
                            if user_id not in list(Cast.objects.filter(performance_id=performance.id).values('user_id')):
                                username = User.objects.get(id=user_id).username
                                c = Cast.objects.create(performance=performance, user_id=user_id, is_user=True, name=User.objects.get(id=user_id).username)
                                print(c, c.name)
                                user_casts.append({'user_id': user_id,'username': username})
                        print(user_casts)
                    # o -> x
                    for origin_cast in origin_casts:
                        if origin_cast.user_id not in user_ids:
                            origin_cast.delete()
                        if origin_cast.user_id in user_ids:
                            # o -> o
                            username = User.objects.get(id=origin_cast.user_id).username
                            user_casts.append({'user_id': origin_cast.user_id,'username': username})
                        
                    if non_user_names:
                        for non_user_name in non_user_names:
                            # x -> o
                            if not Cast.objects.filter(performance=performance, name=non_user_name).exists():
                                username = non_user_name
                                Cast.objects.create(performance=performance, user_id=GHOST_ID, name=non_user_name)
                                non_user_casts.append({'username':username})
                    # o -> x
                    for origin_cast in origin_casts:
                        if origin_cast.name not in non_user_names:
                            origin_cast.delete()
                        if origin_cast.name in non_user_names:
                            # o -> o
                            non_user_casts.append({'username':origin_cast.name})

                    return Response({"status": "OK", "data": {'cast':{'user':user_casts,'non_user':non_user_casts},**serializer.data}})
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "해당 관리자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def recommend_performance(request):
    # 회원가입 정보 기반
    q = Q()
    for category in request.user.like_categories.all():
        q |= Q(category_id=category.id)
    latest_performances = sample(list(Performance.objects.filter(q).filter(end_date__gte=datetime.datetime.today().date())), 1) # 개수 지정
    # 활동 기반(AI - 추후..)
    # pass
    serializer = PerformanceListSerializer(latest_performances, many=True)
    return Response({"status": "OK", "data": serializer.data})


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
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"status": "OK", "data": serializer.data})
        else:
            return Response({"status": "FAIL", "error_msg": "본인 Review만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
