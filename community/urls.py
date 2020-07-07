from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_or_create),
    path('<int:article_id>/', views.detail_or_update_or_delete),
    path('<int:article_id>/comments/', views.comment_list_or_create),
    path('<int:article_id>/comments/<int:comment_id>/', views.comment_update_or_delete),
]
