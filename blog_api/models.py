from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    photo = models.ImageField(upload_to="photos/blogs", null=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(User, related_name="likedblog", blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def like_count(self):
        return self.like_users.count()
