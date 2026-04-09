from django.contrib import admin
from .models import SurgicalGuide


class SurgicalGuideAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'preferred_implant_company',
        'implant_name',
        'created_at',
    )

    search_fields = (
        'preferred_implant_company',
        'implant_name',
        'desired_implant_location',
    )


admin.site.register(SurgicalGuide, SurgicalGuideAdmin)