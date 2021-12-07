from django import forms
from django.core.exceptions import DisallowedHost 

from .models import Disease, Testimonial

class DiseaseForm(forms.ModelForm): 
    class Meta:
        model = Disease
        fields = ['description','causes','prevention','treatment']

        widgets = {
            'description': forms.Textarea(attrs = {'cols':100,'rows':7, 'class': 'p-3'}),
            'prevention': forms.Textarea(attrs = {'cols': 100, 'rows': 7, 'class': 'p-3'}),
            'causes': forms.Textarea(attrs = {'cols':100,'rows':7, 'class': 'p-3'}),
            'treatment': forms.Textarea(attrs = {'cols': 100, 'rows': 7, 'class': 'p-3'}),
            # 'name': forms.Textarea(attrs = {'disabled':'disabled'})
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['description',]
        widgets = {
            'description': forms.Textarea(attrs = {'cols': 100, 'rows':10, 'class': 'p-3'}),
        }