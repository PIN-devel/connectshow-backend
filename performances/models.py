from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

from accounts.models import Club


class Category(models.Model):
    name = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_categories')

    def __str__(self):
        return self.name

    @classmethod
    def init_category(cls):
        CATEGORIES=[
            '음악/콘서트',
            '뮤지컬/오페라',
            '연극',
            '국악',
            '무용/발레',
            '아동/가족',
            '전시',
            '기타'
            ]
        for category in CATEGORIES:
            cls.objects.create(
                name=category
            )


class Performance(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    running_time = models.IntegerField()
    time = models.CharField(max_length=200)
    poster_image = models.ImageField(default='/images/default_user.jpeg')
    image_thumbnail = ImageSpecField(source='poster_image',
                              processors=[ResizeToFit(150, 150)],
                              format='JPEG',
                              options={'quality': 60},
                              )
    description = RichTextUploadingField(blank=True,null=True)
    url = models.CharField(max_length=500)
    avg_rank = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    clubs = models.ManyToManyField(Club, related_name='performances')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_performances')
    casts = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Cast',related_name='performances')

class Review(models.Model):
    point = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Cast(models.Model):
    performance = models.ForeignKey(Performance,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_user = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=True)
