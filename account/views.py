 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,  UserPassesTestMixin
from django.http import JsonResponse
# from django.core import serializers 
from django.db.models import Count, Sum
import datetime
from django.contrib.auth.models import Group

from numpy import insert 

from predict.models import History, Disease
from account.forms import PdfGenForm, UserEditForm
from account.utils import render_to_pdf
from news.models import Post, Subscribe
from news.forms import NewsPostForm
from account.decorators import onlyAllowNonAuthenticated

@onlyAllowNonAuthenticated
def register_user(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'normal-user')
            user.groups.add(group)
            user.save()
            messages.success(request, 'New user is created successfully !!!') 
            return redirect("account:login")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
            

""" History """
class MyProfile( LoginRequiredMixin, TemplateView):
    template_name = "registration/myprofile.html"

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['is_adminuser'] = self.request.user.groups.filter(name__in = ['admin-user']).exists()
        # print(context['is_adminuser'])
        return context 
    
class MyHistoryView(View):
    
    def get(self, request, *args, **kwargs): 
        return render(request, 'registration/myhistory.html', {
            'myhistory_list': request.user.user_history.all().order_by('-date_time')
        })

class HistoryDetailView( LoginRequiredMixin, DetailView): 
    template_name = "registration/historyDetail.html"
    model = History
    context_object_name = 'history' 
    pk_url_kwarg = 'historyId'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user or request.user.is_superuser:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return JsonResponse({}, status=403)

""" All Histories """

class SuperuserRequiredMixin(UserPassesTestMixin):

    def test_func(self): 
        return self.request.user.is_superuser

class HistoryListView( LoginRequiredMixin, SuperuserRequiredMixin, ListView): 
    http_method_names = ['get',]
    template_name = 'registration/admin/allHistory.html'
    model = History 
    context_object_name = 'history_list' 

    def get_queryset(self):
        return History.objects.select_related('user').order_by('-date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today_count'] = History.objects.filter(date_time__date = datetime.date.today()).count()
        return context

class DashboardReportView(LoginRequiredMixin, SuperuserRequiredMixin, View):

    def get(self, request, *args, **kwargs): 
        return JsonResponse({
            'history_list': list(History.objects.values('date_time__date').annotate(Count('id')) ),
        }, status=200)


""" PDF gen"""

class PdfReportReservationView2(View):

    def get(self, request, *args, **kwargs):  
        form = PdfGenForm(self.request.GET) 

        if form.is_valid():
            fromDate = form.cleaned_data.get('fromDate')
            toDate = form.cleaned_data.get('toDate')

            if fromDate and toDate:
                records = History.objects.filter(date_time__date__range=[fromDate, toDate]) 
            elif fromDate or toDate:
                if fromDate: 
                    records = History.objects.select_related('user').filter(date_time__date=fromDate)
                else: 
                    records = History.objects.select_related('user').filter(date_time__date=toDate)
            else: 
                records = History.objects.select_related('user').all()
           
            template_name = "registration/stats/pdf.html"
            return render_to_pdf(
                template_name,
                    {
                        'record': records.order_by('-date_time'),
                        'datetime': datetime.datetime.now(), 
                        'fromDate': fromDate,
                        'toDate': toDate,
                        'redirect_url': request.get_full_path() 
                    }
                ) 
        return JsonResponse({'errors': form.errors, 'status':200})    

""" Admin News part"""
 
class AllNewsView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/admin/allNews.html', {
            "news_list": Post.objects.select_related('author').all().order_by('-created')
        })
class AddNewsView( View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/admin/addNewsForm.html', {
            'form': NewsPostForm
        })
    
    def post(self, request, *args, **kwargs):
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                author = request.user,
                content = form.cleaned_data['content'],
                title = form.cleaned_data['title'],
                image = form.cleaned_data['image'],
            ) 
            messages.success(request, 'News added successfully.')
            return JsonResponse({}, status=200)
         
        return JsonResponse({'errors': form.errors}, status=400)

    
""" All Disease """
class AllDiseaseView(LoginRequiredMixin, View):

    def get(self, request, *args,**kwargs): 
        return render(request, 'registration/admin/allDiseaseAdmin.html', {
            'disease_list': Disease.objects.all().order_by('name')
        })

""" Edit User Account Data """

class UserEditView(LoginRequiredMixin, View):

    def get(self, request, *args,**kwargs):
        form = UserEditForm(instance = request.user)
        return render(request, 'registration/editProfile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User informations updated successfully.') 
            return JsonResponse({}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)

""" All Disease """
class AllSubscribersView(LoginRequiredMixin, View):

    def get(self, request, *args,**kwargs):  
        # print(Subscribe.objects.all().order_by('-id'))
        return render(request, 'registration/admin/allSubscribers.html', {
            'subscriber_list': Subscribe.objects.all().order_by('-id')
        })

class SubscriberDetailsView(LoginRequiredMixin, View):

    def get(self, request,id, *args,**kwargs):   
        obj = get_object_or_404(Subscribe, id= id) 
        return render(request, 'registration/subscribeDetail.html', {
            'subscribe': obj 
        })

class SubscriberDetailDeleteView(LoginRequiredMixin, View):

    def post(self, request, id, *args,**kwargs):   
        obj = get_object_or_404(Subscribe, id= id)
        messages.info(request, f'{obj.email} subscribed email deleted successfully')
        obj.delete()
        return JsonResponse({}, status=200)