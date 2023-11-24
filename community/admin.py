from django.contrib import admin
from community.models import Question, Comment


class QuestionCheck(admin.ModelAdmin):
    list_display = ('id', 'user' , 'question_title', 'created_at')
    search_fields = ('user', 'question_title')
    ordering = ('-created_at',)


class CommentCheck(admin.ModelAdmin):
    list_display = ('id', 'question', 'comment_content', 'created_at')
    search_fields = ('question', 'comment_content')
    ordering = ('-created_at',)

admin.site.register(Question, QuestionCheck)
admin.site.register(Comment, CommentCheck)