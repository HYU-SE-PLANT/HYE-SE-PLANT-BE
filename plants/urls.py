from django.urls import path
from .views import *


urlpatterns = [
    path('', PlantList.as_view()),
    path('create', PlantCreate.as_view()),
    path('type', PlantType.as_view()),
    path('plant_detail', PlantDetail.as_view()),
]
