from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class ClassDateTime(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class Symptom(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    
    def __str__(self):
        return self.name 


class Disease(ClassDateTime):
    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField(null=True, blank=True)
    disease_symptom = models.ManyToManyField(Symptom, blank=True)
    prevention = models.TextField(default="", null=True, blank=True)
    causes = models.TextField(default = "", null=True, blank=True)
    treatment = models.TextField(default = "", null=True, blank=True) 
    # modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Testimonial(ClassDateTime):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.description[:20]}"