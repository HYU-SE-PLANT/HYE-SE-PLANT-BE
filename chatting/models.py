from django.db import models
# from plants.models import Plant


class PlantReplier(models.Model):
    # id = models.AutoField(primary_key=True, null=False, blank=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # chatting_content = models.TextField(null=False, blank=False)
    # is_user_chat = models.BooleanField(default=False, null=False)
    # plant = models.ForeignKey(Plant, null=False, blank=False, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField()