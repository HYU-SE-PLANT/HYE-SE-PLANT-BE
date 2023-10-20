from django.db import models


class Chat(models.Model):
    prompt = models.TextField(),
    response = models.TextField(),
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.prompt