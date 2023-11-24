# 질문에 댓글이 존재하는지 판단 - 반환값: true/false
def get_question_is_answered(question):
    return hasattr(question, 'comment')