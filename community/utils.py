from .models import Comment


# 질문에 댓글이 존재하는지 판단 - 반환값: true/false
def get_question_is_answered(question):
    try:
        Comment.objects.get(question=question)
        return True
    except Comment.DoesNotExist:
        return False