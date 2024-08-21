 
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    #path('',include('basics.urls')),
    path('',include('BO2.urls')),

    path('',include('BO1.urls')),
    path('admin/', admin.site.urls),
]
