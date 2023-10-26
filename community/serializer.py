from .models import Community
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):
    # user_name 받아올 것
    question_id = serializers.ReadOnlyField(source = 'user.user_name')
    class Meta:
        model = Community
        # 표시되는 항목
        fields = ['id', 'question_title', 'question_date', 'questioner_id', 'question_content']