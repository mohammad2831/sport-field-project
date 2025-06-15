from django.urls import path, include
from . import views

app_name= 'main'
urlpatterns =[
    path('', views.InfoOneView.as_view(), name="info_one"),
    path('question/1/', views.QuestonInitialView.as_view(), name="initial_question"),
    path('question/<int:id_q>/', views.QuestionView.as_view(), name="qustion"),
  
]