from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title[:15]


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    youtube_id = models.CharField(max_length=255, default=title)
