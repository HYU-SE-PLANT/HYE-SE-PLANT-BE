from django.db import models
from accounts.models import User


class Plant_Type(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    plant_name = models.CharField(max_length=30, null=False, blank=False)
    plant_temperature = models.CharField(max_length=30, null=False, blank=False)
    plant_humidity = models.CharField(max_length=30, null=False, blank=False)
    plant_illuminance = models.CharField(max_length=30, null=False, blank=False)
    plant_bloom_season = models.CharField(max_length=30, null=False, blank=False)
    plant_watering_cycle = models.CharField(max_length=30, null=False, blank=False)
    plant_difficulty = models.CharField(max_length=10, null=False, blank=False)
    plant_caution = models.CharField(max_length=255, null=False, blank=False)
    germination_period_start = models.IntegerField(null=False, blank=False)
    germination_period_end = models.IntegerField(null=False, blank=False)
    growth_period_start = models.IntegerField(null=False, blank=False)
    growth_period_end = models.IntegerField(null=False, blank=False)
    harvest_period_start = models.IntegerField(null=False, blank=False)
    harvest_period_end = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return self.plant_name


class Plant_Disease_Type(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    plant_disease_name = models.CharField(max_length=100, null=False)
    plant_disease_symptom = models.CharField(max_length=255, null=False)
    plant_disease_condition = models.CharField(max_length=255, null=False)
    
    def __str__(self):
        return self.plant_disease_name


class Plant(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    plant_nickname = models.CharField(max_length=255, null=False, blank=False)
    plant_picture_url = models.CharField(max_length=255, null=False, blank=False)
    plant_type_id = models.ForeignKey(Plant_Type, null=False, blank=False, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(null=False, blank=False)
    harvested_at = models.DateTimeField(null=True)
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.plant_nickname
    
    
class Plant_Disease_Record(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnose_photo_url = models.CharField(max_length=255, null=False, blank=False)
    plant_id = models.ForeignKey(Plant, null=False, blank=False, on_delete=models.CASCADE)
    disease_id = models.ForeignKey(Plant_Disease_Type, null=False, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.created_at