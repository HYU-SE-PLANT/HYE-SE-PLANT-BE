from django.urls import path
from .views import *


urlpatterns = [
    path('', PlantList.as_view()),
]
