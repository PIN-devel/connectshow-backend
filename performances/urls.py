
from django.urls import path

urlpatterns = [
    # performances
    path('', views.list_or_create),
    path('<int:performance_id>/', views.detail_or_delete_or_update),
    path('<int:performance_id>/user/', views.performance_user_valid),
    # reviews
    path('<int:performance_id>/review/<int:review_id>/', views.review_list_or_create),
    path('review/<int:review_id>/', views.review_update_or_delete),
    path('review/<int:review_id>/user/', views.review_user_valid),
]
