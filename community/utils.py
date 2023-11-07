from .models import Comment


# 질문에 댓글이 달려있는지 확인
def get_question_is_answered(question):
    return Comment.objects.filter(question=question).exists