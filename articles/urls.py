from django.urls import path
from .views import *


urlpatterns = [
    path('', ArticleList.as_view()),
]
