from django.urls import path
from recipes.views import *
  

urlpatterns = [
    path('', home),
    path('recipe/<int:id>/',recipe),
]

