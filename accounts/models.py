from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

from django.conf import settings



class Club(models.Model):
    master = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    club_name = models.CharField(max_length=50)
    club_image = models.ImageField(default='/images/default_user.jpeg')
    club_image_thumbnail = ImageSpecField(source='club_image',
                              processors=[ResizeToFit(150, 150)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(AbstractUser):
    profile_image = models.ImageField(default='/images/default_user.jpeg')
    image_thumbnail = ImageSpecField(source='profile_image',
                              processors=[ResizeToFit(150, 150)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    clubs = models.ManyToManyField(Club,through='ClubMember',related_name='members')
    follow_clubs = models.ManyToManyField(Club,related_name='follow_users')

class ClubMember(models.Model):
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_member = models.BooleanField(default=False)