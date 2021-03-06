from django.urls import path
from . import views

urlpatterns = [
    # performances
    path('', views.list_or_create),
    path('<int:performance_id>/', views.detail_or_delete_or_update),
    path('recommendations/', views.recommend_performance),
    path('<int:performance_id>/like/', views.like_performance),
    path('club/<int:club_id>/', views.club_performance),
    path('category/', views.category),

    # reviews
    path('<int:performance_id>/reviews/', views.review_list_or_create),
    path('reviews/<int:review_id>/', views.review_update_or_delete),

    # calendar
    path('calendar/', views.calendar),
]