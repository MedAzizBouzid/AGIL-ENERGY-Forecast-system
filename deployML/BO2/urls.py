from django.urls import path
from . import views

urlpatterns=[
     
    path('bo2',views.predictor,name='bo2'),
    path('result_bo2',views.formInfo,name='result_bo2')

]