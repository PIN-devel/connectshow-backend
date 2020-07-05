from django.db import models
from django.conf import settings
# Create your models here.

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

class Category(models.Model):
    name = models.CharField(max_length=50)

class Performance(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    poster_image = models.ImageField(default='/images/default_user.jpeg')
    image_thumbnail = ImageSpecField(source='poster_image',
                              processors=[ResizeToFit(150, 150)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    description = models.TextField()
    url = models.CharField(max_length=100)
    avg_rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Review(models.Model):
    point = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
