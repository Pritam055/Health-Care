from django.urls import path

from . import views 

app_name = "predict"
urlpatterns = [ 
    path('', views.index, name="index"),
    path('search/', views.DiseaseSearchView.as_view(), name='disease_search'),
    path('disease/<int:id>/detail/', views.disease_detail, name="disease_detail"),
    path('disease/<int:pk>/update/', views.DiseaseUpdateView.as_view(), name="disease_update"),
    path('disease-list/', views.DiseaseListView.as_view(), name="disease_list"),
    path('testimonials/', views.TestimonialListView.as_view(), name="testimonials"),
    path('testimonials/<int:pk>/update/', views.TestimonialEditView.as_view(), name="testimonial_update"),
    path('testimonials/add/', views.TestimonialCreateView.as_view(), name="testimonial_add"),
    path('testimonials/<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name="testimonial_delete"),
    

]