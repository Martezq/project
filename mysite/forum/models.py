from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def latest_post(self):
    #     return self.post_set.order_by('-created_at').first()
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.user}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
