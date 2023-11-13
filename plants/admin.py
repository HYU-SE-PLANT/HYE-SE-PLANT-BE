from django.contrib import admin
from plants.models import *


# Register your models here.
class PlantCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_nickname', 'user_id', 'plant_type_id', 'planted_at', 'harvested_at')


class PlantDiseaseTypeCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_disease_name')
    
    
class PlantDiseaseRecordCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_id', 'disease_id', 'created_at')
    fieldsets = ((None, {'fields': ('plant_id', 'disease_id')}),)

admin.site.register(Plant, PlantCheck)
admin.site.register(Plant_Type)
admin.site.register(Plant_Disease_Type, PlantDiseaseTypeCheck)
admin.site.register(Plant_Disease_Record, PlantDiseaseRecordCheck)