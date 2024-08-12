from django.urls import path
from . import views

urlpatterns=[
     
    path('bo1',views.predictor,name='bo1'),
    path('result',views.formInfo,name='result')

]