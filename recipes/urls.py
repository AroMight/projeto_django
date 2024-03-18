from django.urls import path
from recipes.views import *
  

urlpatterns = [
    path('', home),
    path('contacts/', contact),
    path('about/', about)
]