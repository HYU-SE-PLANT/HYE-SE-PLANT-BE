from django.urls import path
from .views import PlantChatting


urlpatterns = [
    path('chat/', PlantChatting.as_view()),
]
