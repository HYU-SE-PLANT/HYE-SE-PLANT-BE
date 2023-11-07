from django.urls import path
from .views import *


urlpatterns = [
    path('', PlantList.as_view()),
    path('create/', PlantCreate.as_view()),
    path('type/', PlantType.as_view()),
    # path('<int:pk>/', PlantDetail.as_view()),
    path('<str:account_id>/<str:plant_nickname>/', PlantDetail.as_view()),
]
