from django.urls import path, include

from . import views 

app_name="account"
urlpatterns = [ 
    path('register', views.register_user, name="register"),
    path('', include('django.contrib.auth.urls'))

]