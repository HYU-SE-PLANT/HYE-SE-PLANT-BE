from django.db import models
from django.conf import settings
from accounts.models import User


class Community(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) # 게시글의 id 값
    question_title = models.CharField(max_length=255, null=False, blank=False) # 제목 길이: 최대 255자
    question_content = models.TextField(null=False, blank=False) # 내용 입력
    question_date = models.DateTimeField(auto_now_add=True) # 작성 날짜
    answer_or_not = models.BooleanField(default=False) # 답변 여부
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE) # 작성자