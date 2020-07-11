from django.urls import path
from . import views


urlpatterns = [
    path('<int:club_id>/', views.list_or_create),
    path('articles/<int:article_id>/', views.detail_or_update_or_delete),
    path('<int:article_id>/comments/', views.comment_list_or_create),
    path('comments/<int:comment_id>/', views.comment_update_or_delete),
]
