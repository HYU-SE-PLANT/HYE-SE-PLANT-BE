from .models import Community, Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'question', 'created_at', 'comment_content']
        extra_kwargs = {
            'question': {
                'required': False
            }
        }


class CommunitySerializer(serializers.ModelSerializer):
    # account_id 받아올 것
    user = serializers.ReadOnlyField(source = 'user.account_id')
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Community
        # 표시되는 항목
        fields = ['id', 'question_title', 'created_at', 'user', 'question_content', 'comments']