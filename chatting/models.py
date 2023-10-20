from django.db import models


class PlantReplier(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()