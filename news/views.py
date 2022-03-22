from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib import messages 
from django.http import JsonResponse

from .models import Post, Subscribe
from .forms import SubscribeForm
# Create your views here.

"""class NewsMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff: 
            return super().dispatch(request, *args, **kwargs)
        return redirect(  )"""

class NewsHomeView(ListView):
    template_name = "news/all_news.html"
    model = Post 
    ordering = ['-created',]
    context_object_name = "posts" 

class NewsDetailView(DetailView):
    model = Post 
    context_object_name = "post"
    template_name= "news/news_details.html"


class SubscribeView(View): 
    
    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            # form.save()
            print(form.cleaned_data)
            # messages.success(request, 'Subscribed successfully.')
            return JsonResponse({}, status=200)
        
        print(form.errors)
        return JsonResponse({'errors': form.errors}, status=400)


