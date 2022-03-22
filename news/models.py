from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify

from predict.models import ClassDateTime
# Create your models here.

class Post(ClassDateTime):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    image = models.ImageField(upload_to="posts")
    slug = models.SlugField(max_length = 255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "posts" )

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

class Subscribe(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250, unique=True)

    def __str__(self):
        return self.email

    
