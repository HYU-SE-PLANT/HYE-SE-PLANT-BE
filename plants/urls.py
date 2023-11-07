from django.urls import path
from .views import *


urlpatterns = [
    path('', PlantList.as_view()),
    path('create/', PlantCreate.as_view()),
    paht('type/', PlantType.as_view()),
]
