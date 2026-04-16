from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import SurgicalGuideForm
from .models import SurgicalGuide
from django.core.files.base import ContentFile
# from weasyprint import HTML
import io
import threading
import uuid
import requests

# Create your views here.

def generate_pdf_background(instance_id):
    try:
        instance = SurgicalGuide.objects.get(id=instance_id)

        # Prepare data to send to API
        payload = {
            "preferred_implant_company": instance.preferred_implant_company,
            "implant_name": instance.implant_name,
            "jaw_information": instance.jaw_information,
            "prosthetic_plan": instance.prosthetic_plan,
            "desired_implant_location": instance.desired_implant_location,
            "preferred_size": instance.preferred_size,
            "ap_spread_angle_implant": instance.ap_spread_angle_implant,
            "immediate_extractions": instance.immediate_extractions,
            "immediate_extractions_notes": instance.immediate_extractions_notes,
            "bone_grafting": instance.bone_grafting,
            "bone_grafting_notes": instance.bone_grafting_notes,
            "bone_reduction": instance.bone_reduction,
            "bone_reduction_notes": instance.bone_reduction_notes,
            "surgical_drill_kit": instance.surgical_drill_kit,
            "surgery_date": str(instance.surgery_date) if instance.surgery_date else "",
            "provisional_planning": instance.provisional_planning,
        }

        # Call API
        response = requests.post(
            "https://api.advancedentalexport.com/generate-pdf/",
            json={"data": payload},
            timeout=60
        )

        if response.status_code == 200:
            pdf_content = response.content

            filename = f"surgical_guide_{instance_id}_{uuid.uuid4().hex[:8]}.pdf"

            # Save PDF to model
            instance.pdf_document.save(filename, ContentFile(pdf_content))

            # Send Email
            email_msg = EmailMessage(
                subject=f'New Surgical Guide Submitted (ID: #{instance_id})',
                body='PDF attached.',
                from_email=settings.EMAIL_HOST_USER,
                to=['vaghela9632@gmail.com'],
            )
            email_msg.attach(filename, pdf_content, 'application/pdf')
            email_msg.send(fail_silently=False)

        else:
            print("API ERROR:", response.text)

    except Exception as e:
        print("PDF API ERROR:", e)

def surgical_guide(request):
    if request.method == "POST":
        form = SurgicalGuideForm(request.POST)

        if form.is_valid():
            instance = form.save()

            # Start background thread to generate PDF
            thread = threading.Thread(target=generate_pdf_background, args=(instance.id,))
            thread.start()

            return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = SurgicalGuideForm()

    return render(request, 'surgical_guide.html', {'form': form, 'product': None})