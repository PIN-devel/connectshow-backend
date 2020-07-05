from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail


class User(AbstractUser):
    profile_image = models.ImageField(default='/images/default_user.jpeg')
    image_thumbnail = ImageSpecField(source='profile_image',
                              processors=[ResizeToFit(150, 150)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    # like_category =

class Club(models.Model):
    club_name = models.CharField(max_length=50)
    club_image = models.ImageField(default='/images/default_user.jpeg')
    club_image_thumbnail = ImageSpecField(source='club_image',
                              processors=[ResizeToFit(150, 150)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)