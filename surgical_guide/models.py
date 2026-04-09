from django.db import models

# Create your models here.

class SurgicalGuide(models.Model):
    preferred_implant_company = models.CharField(max_length=255, blank=True, null=True)
    implant_name = models.CharField(max_length=255, blank=True, null=True)
    JAW_CHOICES = [
        ('maxilla', 'Maxilla'),
        ('mandible', 'Mandible'),
    ]
    jaw_information = models.JSONField(blank=True, null=True)
    prosthetic_plan = models.TextField(blank=True, null=True)
    desired_implant_location = models.CharField(max_length=255, blank=True, null=True)
    preferred_size = models.CharField(max_length=255, blank=True, null=True)
    ap_spread_angle_implant = models.CharField(max_length=255, blank=True, null=True)
    immediate_extractions = models.BooleanField(null=True, blank=True)
    immediate_extractions_notes = models.CharField(max_length=255, blank=True, null=True)
    bone_grafting = models.BooleanField(null=True, blank=True)
    bone_grafting_notes = models.CharField(max_length=255, blank=True, null=True)
    bone_reduction = models.BooleanField(null=True, blank=True)
    bone_reduction_notes = models.CharField(max_length=255, blank=True, null=True)
    surgical_drill_kit = models.CharField(max_length=255, blank=True, null=True)
    provisional_planning = models.TextField(blank=True, null=True)
    surgery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Surgical Guide #{self.id}"
    
