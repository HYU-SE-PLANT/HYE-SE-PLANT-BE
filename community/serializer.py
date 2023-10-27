from .models import Community, Comment
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):
    # account_id 받아올 것
    user = serializers.ReadOnlyField(source = 'user.account_id')
    class Meta:
        model = Community
        # 표시되는 항목
        fields = ['id', 'question_title', 'question_date', 'question_updated_date', 'user', 'question_content', 'answer_or_not']
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'question', 'comment_date', 'comment_content']