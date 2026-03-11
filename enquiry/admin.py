from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import *
# Register your models here.
# Register your models here.



@admin.action(description="download selected contact as CSV")
def export_contacts_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)

    #header
    writer.writerow(['Name','Email','Phone','Date', 'Message'])

    #data of the rows
    for contact in queryset:
        writer.writerow([
            contact.name,
            contact.email,
            contact.contact,
            contact.city,
            contact.date.strftime("%Y-%m-%d") if contact.date else "",
            contact.message,
        ])
    return response
class ContactAdmin(admin.ModelAdmin):
    list_display=['email', 'date','city', 'message', "formatted_created_at"]
    search_fields = ['email', 'name', 'city']
    actions = [export_contacts_csv]
    def formatted_created_at(self, obj):
        if obj.created_at:
            return timezone.localtime(obj.created_at).strftime("%d-%m-%Y %I:%M %p")
        return "-"
    formatted_created_at.short_description = "Submitted At"
    
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact', 'date']
    search_fields = ['name', 'email', 'contact']
    list_filter = ['date']


class CareerFileAdmin(admin.ModelAdmin):
    list_display = ['career', 'resume', 'date']
    list_filter = ['date']

admin.site.register(NewsLetter)
admin.site.register(Review)
admin.site.register(Contact, ContactAdmin)
admin.site.register(InstaPost)
admin.site.register(STLFile)
admin.site.register(STLFileData)
admin.site.register(Career, CareerAdmin)
admin.site.register(CareerFile, CareerFileAdmin)
