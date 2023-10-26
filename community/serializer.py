from .models import Community
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):
    # account_id 받아올 것
    user = serializers.ReadOnlyField(source = 'user.account_id')
    class Meta:
        model = Community
        # 표시되는 항목
        fields = ['id', 'question_title', 'question_date', 'question_updated_date', 'user', 'question_content']