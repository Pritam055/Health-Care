from django.contrib import admin

from .models import Disease, Symptom, Testimonial
# Register your models here.

admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(Testimonial)