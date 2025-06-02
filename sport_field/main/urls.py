from django.urls import path, include
from . import views

app_name= 'main'
urlpatterns =[
    path('', views.InfoOneView.as_view(), name="info_one"),
    path('personal/', views.PersonalInfoView.as_view(), name="info_personal"),
  
]