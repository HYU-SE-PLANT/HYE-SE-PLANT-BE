from django.db import models


class PlantReplier(models.Model):
    user_input = models.TextField()
    chatgpt_output = models.TextField()