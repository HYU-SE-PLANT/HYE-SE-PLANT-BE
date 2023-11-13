from django.contrib import admin
from plants.models import *


# Register your models here.
class PlantDiseaseTypeCheck(admin.ModelAdmin):
    list_display = ('id', 'plant_disease_name')

admin.site.register(Plant)
admin.site.register(Plant_Type)
admin.site.register(Plant_Disease_Type, PlantDiseaseTypeCheck)
admin.site.register(Plant_Disease_Record)