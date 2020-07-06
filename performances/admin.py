from django.contrib import admin

from .models import Performance, Review, Category

admin.site.register(Category)
admin.site.register(Performance)
admin.site.register(Review)
