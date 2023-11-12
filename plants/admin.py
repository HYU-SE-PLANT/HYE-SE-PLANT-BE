from django.contrib import admin
from plants.models import *


# Register your models here.
admin.site.register(Plant)
admin.site.register(Plant_Type)
admin.site.register(Plant_Disease_Type)
admin.site.register(Plant_Disease_Record)