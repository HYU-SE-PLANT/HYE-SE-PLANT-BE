from django.urls import path
from .views import *


urlpatterns = [
    path('', QuestionList.as_view()),
    path('create', QuestionCreate.as_view()),
    path('question_detail', QuestionDetail.as_view()),
    path('comment', CommentCreate.as_view()),
]
