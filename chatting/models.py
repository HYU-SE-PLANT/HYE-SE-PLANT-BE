from django.db import models


class Chat(models.Model):
    user_input = models.TextField()
    gpt_response = models.TextField(blank=True, null=True)