from django.urls import path
from .views import *


urlpatterns = [
    path('', QuestionList.as_view()),
    path('create/', QuestionCreate.as_view()),
    path('', QuestionDetail.as_view()),
    path('<int:pk>/comment/', CommentCreate.as_view()),
]
