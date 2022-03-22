from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
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
 

class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,  on_delete=models.CASCADE, related_name="user_history")
    max_prob_disease = models.CharField(max_length = 100)
    percentage = models.DecimalField(decimal_places=2, max_digits=4)
    date_time = models.DateTimeField(auto_now_add=True)
    symptoms = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Histories"

    def __str__(self):
        return f"{self.user.username} - {self.max_prob_disease}"