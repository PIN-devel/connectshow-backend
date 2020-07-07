from django.urls import path
from . import views

urlpatterns = [
    path('', views.identify),
    path('<int:user_id>/', views.detail_or_delete_or_update),
    path('clubs/', views.club_list_or_create),
    path('clubs/<club_id>/', views.club_detail_or_delete_or_update),
    path('clubs/<club_id>/apply/', views.club_subscribe_or_cancle_or_withdraw),
    path('clubs/<club_id>/user/<user_id>/',
         views.club_accept_or_refuse_or_expel),
    path('clubs/<club_id>/follow/', views.club_follow),
]
