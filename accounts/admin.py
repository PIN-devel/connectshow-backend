from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Club, ClubMember
# Register your models here.
admin.site.register(get_user_model())
admin.site.register(Club)
admin.site.register(ClubMember)

