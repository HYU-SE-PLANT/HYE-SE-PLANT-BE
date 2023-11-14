from django.contrib import admin
from plants.models import *
from django.utils import timezone
from .utils import calculate_growth_level


# Register your models here.
class PlantCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_nickname', 'days_since_planted', 'growth_level', 'user_id', 'plant_type_id', 'planted_at', 'harvested_at')
    
    def days_since_planted(self, obj):
        today = timezone.now().date()
        return (today - obj.planted_at.date()).days
    
    def growth_level(self, obj):
        return calculate_growth_level(obj.plant_type_id, obj.planted_at)


class PlantDiseaseTypeCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_disease_name')
    
    
class PlantDiseaseRecordCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_id', 'disease_id', 'created_at')
    fieldsets = ((None, {'fields': ('plant_id', 'disease_id')}),)

admin.site.register(Plant, PlantCheck)
admin.site.register(Plant_Type)
admin.site.register(Plant_Disease_Type, PlantDiseaseTypeCheck)
admin.site.register(Plant_Disease_Record, PlantDiseaseRecordCheck)