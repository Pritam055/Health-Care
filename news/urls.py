from django.urls import path 

from . import views 

app_name = "news"
urlpatterns = [ 
    path('', views.NewsHomeView.as_view(), name="home"),
    path('details/<int:pk>', views.NewsDetailView.as_view(), name="news_detail"),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    

]