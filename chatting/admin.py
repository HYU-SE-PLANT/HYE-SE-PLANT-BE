from django.contrib import admin
from chatting.models import PlantReplier


class PlantChattingCheck(admin.ModelAdmin):
    list_display = ('created_at', 'chatting_content', 'is_user_chat', 'plant_id')
    
admin.site.register(PlantReplier, PlantChattingCheck)