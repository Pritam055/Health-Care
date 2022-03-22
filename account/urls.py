from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from account import views 
from account.decorators import onlyAllowNonAuthenticated

app_name="account"
urlpatterns = [ 
    
    # path('', include('django.contrib.auth.urls')),
    path('login/', onlyAllowNonAuthenticated(LoginView.as_view()), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_user, name="register"),
    path('myprofile/', views.MyProfile.as_view(), name="myprofile"),
    path('myhistory/', views.MyHistoryView.as_view(), name='myhistory'),
    path('history-detail/<int:historyId>/', views.HistoryDetailView.as_view(), name='history_detail'),
    path('update-user-info/', views.UserEditView.as_view(), name='update_user'),

    path('admin/all-histories/', views.HistoryListView.as_view(),name='all_histories'),
    path('admin/history-report/', views.DashboardReportView.as_view(), name='history_report'),
    path('admin/pdf-report-gen/', views.PdfReportReservationView2.as_view(), name='pdf_report_gen'),
    path('admin/all-news/', views.AllNewsView.as_view(), name='all_news' ),
    path('admin/add-news/', views.AddNewsView.as_view(), name='add_news'),
    path('admin/all-disease/', views.AllDiseaseView.as_view(), name='all_disease'),    



]