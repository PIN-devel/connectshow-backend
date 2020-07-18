from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserIdentifySerializer, ClubSerializer
from .models import Club, ClubMember


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def identify(request):
    serializer = UserIdentifySerializer(request.user)
    return Response({"status": "OK", "data": serializer.data})


# Create your views here.
@api_view(['GET', 'DELETE', 'PUT'])
def detail_or_delete_or_update(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)

    # 조회
    if request.method == 'GET':
        return Response({"status": "OK", "data": serializer.data})

    # 삭제
    if request.user.is_authenticated:
        
        if request.method == 'DELETE':
            if request.user == user:
                request.user.delete()
                return Response({"status": "OK", **serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 수정
        else:
            if request.user == user:
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"status": "FAIL", "error_msg": "로그인이 필요한 서비스 입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    # @api_view(['POST'])
    # @permission_classes([IsAuthenticated])
    # def edit(request, user_id):
    #     user = get_object_or_404(User, id=user_id)
    #     if request.user == user:
    #         serializer = UserSerializer(user, data=request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #         return Response({"message": "회원 정보가 수정되었습니다."})
    #     else:
    #         return Response({"message": "사용자 본인만 수정 가능합니다."})


@api_view(['GET', 'POST'])
def club_list_or_create(request):
    user = request.user
    PerPage = 10
    if request.method == 'GET':
        p = request.GET.get('page', 1)
        clubs = Paginator(Club.objects.order_by('-pk'), PerPage)
        serializer = ClubSerializer(clubs.page(p), many=True)
        return Response({"status": "OK", "data": serializer.data})

    else:  # POST
        if user.is_authenticated:
            serializer = ClubSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                club = serializer.save(master=request.user)
                ClubMember.objects.create(
                    user_id=request.user.id, club_id=club.id, is_member=True)
                return Response({"status": "OK", "data": serializer.data})
        else:
            return Response({"status": "FAIL", "error_msg": "로그인이 필요한 서비스 입니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def club_detail_or_delete_or_update(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.method == 'GET':
        # member
        members = ClubMember.objects.filter(club_id=club.id, is_member=True)
        users_serializer = []
        for member in members:
            users_serializer.append(UserIdentifySerializer(member.user).data)
        # non_member
        non_members = ClubMember.objects.filter(club_id=club.id, is_member=False)
        non_users_serializer = []
        for member in non_members:
            non_users_serializer.append(UserIdentifySerializer(member.user).data)
        serializer = ClubSerializer(club)
        return Response({"status": "OK", "data": {'club_members': users_serializer, 'club_waiting_members': non_users_serializer, 'club_detail': serializer.data}})
    
    if request.user.is_authenticated:
        if request.method == 'PUT':
            if request.user == club.master:
                serializer = ClubSerializer(
                    club, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"status": "OK", "data": serializer.data})
            else:
                return Response({"status": "FAIL", "error_msg": "관리자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:  # DELETE
            if request.user == club.master:
                club.delete()
                return Response({"status": "OK"})
            else:
                return Response({"status": "FAIL", "error_msg": "관리자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"status": "FAIL", "error_msg": "로그인이 필요한 서비스 입니다."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def club_subscribe_or_cancle_or_withdraw(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    user = request.user
    master = club.master
    if user == master:
        return Response({"status": "FAIL", "error_msg": "관리자는 접근 할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    else:
        if request.method == 'POST':
            if ClubMember.objects.filter(club_id=club.id, user_id=user.id).exists():
                clubmember = ClubMember.objects.filter(
                    club_id=club.id, user_id=user.id)
                clubmember.delete()
                return Response({"status": "OK"})
            else:
                clubmember = ClubMember.objects.create(
                    club_id=club.id, user_id=user.id)
                data = {
                    "club": club.id,
                    "user": user.id,
                    "is_member": clubmember.is_member
                }
                return Response({"status": "OK", "data": data})
        else:  # DELETE
            clubmember = ClubMember.objects.filter(
                club_id=club.id, user_id=user.id)
            clubmember.delete()
            return Response({"status": "OK"})


@api_view(['POST',  'DELETE'])
@permission_classes([IsAuthenticated])
def club_accept_or_refuse_or_expel(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    master = club.master
    if request.method == 'POST':
        if request.user == master:
            if ClubMember.objects.filter(club_id=club.id, user_id=user.id).exists():
                subscribe_user = ClubMember.objects.get(
                    club_id=club.id, user_id=user.id)
                subscribe_user.is_member = True
                subscribe_user.save()
                data = {
                    "club": club.id,
                    "user": user.id,
                    "is_member": subscribe_user.is_member
                }
                return Response({"status": "OK", "data": data})
            else:
                return Response({"status": "FAIL", "error_msg": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "FAIL", "error_msg": "관리자만 권한이 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    else:  # DELETE
        if request.user == master:
            clubmember = ClubMember.objects.filter(
                club_id=club.id, user_id=user.id)
            clubmember.delete()
            return Response({"status": "OK"})
        else:
            return Response({"status": "FAIL", "error_msg": "관리자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def club_follow(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if club.follow_users.filter(pk=request.user.id).exists():
        club.follow_users.remove(request.user)
        follow = False
    else:
        club.follow_users.add(request.user)
        follow = True
    data = {
        "follow": follow,
        "count": club.follow_users.count()
    }
    return Response({"status": "OK", "data": data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def club_follow_check(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if club.follow_users.filter(pk=request.user.id).exists():
        follow = True
    else:
        follow = False
    data = {
        "follow": follow,
        "count": club.follow_users.count()
    }
    return Response({"status": "OK", "data": data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def club_master_check(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if club.master == request.user:
        master = True
    else:
        master = False
    data = {
        "master": master,
    }
    return Response({"status": "OK", "data": data})