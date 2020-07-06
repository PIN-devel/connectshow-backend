from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Performance, Review, Category

# Create your views here.
def list_or_create(request):
    pass

def detail_or_delete_or_update(request):
    pass

def performance_user_valid(request):
    pass

def review_list_or_create(request):
    pass

def review_update_or_delete(request):
    pass

def review_user_valid(request):
    pass
