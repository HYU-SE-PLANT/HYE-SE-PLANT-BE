from django.urls import path
from .views import PlantChattingView


urlpatterns = [
    path('chat', PlantChattingView.as_view()),
]
