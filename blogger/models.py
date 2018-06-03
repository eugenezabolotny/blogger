from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_posted = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
