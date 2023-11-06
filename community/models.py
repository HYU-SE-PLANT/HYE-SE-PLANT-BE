from django.db import models
from django.conf import settings
from accounts.models import User


class Community(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) # 게시글의 id 값
    question_title = models.CharField(max_length=255, null=False, blank=False) # 제목 길이: 최대 255자
    created_at = models.TextField(null=False, blank=False) # 내용 입력
    created_at = models.DateTimeField(auto_now_add=True) # 작성 날짜
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE) # 작성자
    
    def __str__(self):
        return self.question_title
    
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) # 댓글의 id 값
    question = models.ForeignKey(Community, related_name='comments', null=False, blank=False, on_delete=models.CASCADE) # 질의응답 - 질문
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False) # 댓글 작성 날짜
    comment_content = models.TextField(null=False, blank=False) # 댓글 내용 입력
    
    def __str__(self):
        return self.comment_content
