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
        jaw_info = instance.jaw_information
        if isinstance(jaw_info, list):
            jaw_info = ", ".join(jaw_info)

        def yes_no(value):
            return "Yes" if value else "No"

        # Prepare data to send to API
        payload = {
            "doctor_name": instance.doctor_name,
            "patient_name": instance.patient_name,
            "contact_number": instance.contact_number,
            "preferred_implant_company": instance.preferred_implant_company,
            "implant_name": instance.implant_name,
            "jaw_information": jaw_info,
            "prosthetic_plan": instance.prosthetic_plan,
            "desired_implant_location": instance.desired_implant_location,
            "preferred_size": instance.preferred_size,
            "ap_spread_angle_implant": instance.ap_spread_angle_implant,
            "immediate_extractions": yes_no(instance.immediate_extractions),
            "immediate_extractions_notes": instance.immediate_extractions_notes,
            "bone_grafting": yes_no(instance.bone_grafting),
            "bone_grafting_notes": instance.bone_grafting_notes,
            "bone_reduction": yes_no(instance.bone_reduction),
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
            email_body_html = f"""
                <h2>New Surgical Guide Submission (ID: #{instance_id})</h2>

                <p><strong>Doctor Name:</strong> {instance.doctor_name}</p>
                <p><strong>Patient Name:</strong> {instance.patient_name}</p>
                <p><strong>Contact Number:</strong> {instance.contact_number}</p>
                <p><strong>Jaw Information:</strong> {instance.jaw_information}</p>
                <p><strong>Preferred Implant Company:</strong> {instance.preferred_implant_company}</p>
                <p><strong>Implant Name:</strong> {instance.implant_name}</p>
                <p><strong>Desired Implant Location:</strong> {instance.desired_implant_location}</p>
                <p><strong>Preferred Size:</strong> {instance.preferred_size}</p>
                <p><strong>A/P Spread:</strong> {instance.ap_spread_angle_implant}</p>
                <p><strong>Immediate Extractions:</strong> {instance.immediate_extractions}</p>
                <p><strong>Notes:</strong> {instance.immediate_extractions_notes}</p>
                <p><strong>Bone Grafting:</strong> {instance.bone_grafting}</p>
                <p><strong>Notes:</strong> {instance.bone_grafting_notes}</p>
                <p><strong>Bone Reduction:</strong> {instance.bone_reduction}</p>
                <p><strong>Notes:</strong> {instance.bone_reduction_notes}</p>
                <p><strong>Surgical Drill Kit:</strong> {instance.surgical_drill_kit}</p>
                <p><strong>Surgery Date:</strong> {instance.surgery_date}</p>
                <p><strong>Provisional Planning:</strong><br>{instance.provisional_planning}</p>
                <p><strong>Prosthetic Plan:</strong><br>{instance.prosthetic_plan}</p>
                """
            # Send Email
            email_msg = EmailMessage(
                subject=f'New Surgical Guide Submitted (ID: #{instance_id})',
                body=email_body_html,
                from_email=settings.EMAIL_HOST_USER,
                to=['vaghela9632@gmail.com'],
            )
            email_msg.content_subtype = "html"
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