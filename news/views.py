from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib import messages 
from django.http import JsonResponse

from .models import Post, Subscribe
from .forms import SubscribeForm
from .helpers import send_subscriber_mail
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
    paginate_by = 7

class NewsDetailView(DetailView):
    model = Post 
    context_object_name = "post"
    template_name= "news/news_details.html"


class SubscribeView(View): 
    
    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST) 
        if form.is_valid():
            form.save() 
            try:
                send_subscriber_mail(form.cleaned_data.get('name'), form.cleaned_data.get('email'))
            except Exception as e: 
                # print(e.__str__()) 
                return JsonResponse({'data': e.__str__()}, status=400)
            return JsonResponse({}, status=200)
        
        # print(form.errors)
        return JsonResponse({'errors': form.errors}, status=400)


