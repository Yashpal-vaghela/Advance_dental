from django.contrib import admin
from .models import SurgicalGuide


class SurgicalGuideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'doctor_name',
        'patient_name',
        'implant_name',
        'created_at',
    )

    search_fields = (
        'doctor_name',
        'implant_name',
        'desired_implant_location',
    )


admin.site.register(SurgicalGuide, SurgicalGuideAdmin)