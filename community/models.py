from django.db import models
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

from accounts.models import Club

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(null=True)
    image_thumbnail = ImageSpecField(source='image',
                              processors=[ResizeToFit(width=300)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
